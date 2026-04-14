from __future__ import annotations
import asyncio
import os
from solders.pubkey import Pubkey
from solders.message import Message
from solders.transaction import Transaction
from spl.token.instructions import (
    get_associated_token_address,
    burn,
    BurnParams,
)
from spl.token.constants import TOKEN_PROGRAM_ID
from solana.rpc.commitment import Confirmed
from anchorpy import Program, Provider, Wallet
from anchorpy.idl import Idl

from .constants import (
    PUMPFUN_PROGRAM_ID,
    BONDING_CURVE_SEED,
    SOLSCAN_TX_URL,
    SOLANA_MAINNET_RPC,
)
from .types import LockParams, LockResult
from .wallet import JellychainWallet, create_async_client

_IDL_PATH = os.path.join(os.path.dirname(__file__), "pumpfun_idl.json")


def _load_idl() -> Idl:
    with open(_IDL_PATH, "r") as f:
        return Idl.from_json(f.read())


def derive_bonding_curve_pda(mint: Pubkey) -> tuple[Pubkey, int]:
    return Pubkey.find_program_address(
        [BONDING_CURVE_SEED, bytes(mint)],
        PUMPFUN_PROGRAM_ID,
    )


async def lock_async(
    params: LockParams,
    rpc_url: str = SOLANA_MAINNET_RPC,
) -> LockResult:
    try:
        wallet = JellychainWallet.from_base58(params.private_key_base58)
        mint = Pubkey.from_string(params.mint_address)

        bonding_curve, _ = derive_bonding_curve_pda(mint)

        async with create_async_client(rpc_url) as client:
            idl = _load_idl()
            anchor_wallet = Wallet(wallet.keypair)
            provider = Provider(client, anchor_wallet)
            program = Program(idl, PUMPFUN_PROGRAM_ID, provider)

            try:
                bc_state = await program.account["BondingCurveAccount"].fetch(bonding_curve)
            except Exception:
                return LockResult(
                    success=False,
                    error=f"No bonding curve account found for mint {params.mint_address} — not a valid Pump.fun token",
                )

            if bc_state.complete:
                return LockResult(
                    success=False,
                    error="Bonding curve is complete (token graduated) — lock dev tokens before graduation",
                )

            print(
                f"[JellyChain] Bonding curve: {bonding_curve} "
                f"(virtual reserves: {bc_state.virtual_token_reserves}, verified via Anchor IDL)"
            )

            wallet_ata = get_associated_token_address(wallet.public_key, mint)
            balance_resp = await client.get_token_account_balance(wallet_ata, commitment=Confirmed)

            if not balance_resp.value:
                return LockResult(success=False, error="No token account found for this wallet/mint")

            total_amount = int(balance_resp.value.amount)
            if total_amount == 0:
                return LockResult(success=False, error="No tokens to lock — wallet balance is 0")

            lock_amount = params.amount_tokens if params.amount_tokens else total_amount

            if lock_amount > total_amount:
                return LockResult(
                    success=False,
                    error=f"Requested lock amount {lock_amount} exceeds balance {total_amount}",
                )

            print(
                f"[JellyChain] Burning (locking) {lock_amount} tokens for mint: {params.mint_address}"
            )

            burn_ix = burn(BurnParams(
                program_id=TOKEN_PROGRAM_ID,
                account=wallet_ata,
                mint=mint,
                owner=wallet.public_key,
                amount=lock_amount,
                signers=[],
            ))

            recent_bh_resp = await client.get_latest_blockhash(commitment=Confirmed)
            recent_bh = recent_bh_resp.value.blockhash

            msg = Message.new_with_blockhash([burn_ix], wallet.public_key, recent_bh)
            txn = Transaction([wallet.keypair], msg, recent_bh)

            result = await provider.send(txn)
            tx_sig = str(result)

        print(f"[JellyChain] {lock_amount} tokens burned (locked), TX={tx_sig}")

        return LockResult(
            success=True,
            tx_signature=tx_sig,
            solscan_url=f"{SOLSCAN_TX_URL}/{tx_sig}",
            locked_amount=str(lock_amount),
            lock_type="burn",
        )

    except Exception as exc:
        error_msg = str(exc)
        print(f"[JellyChain] Lock failed: {error_msg}")
        return LockResult(success=False, error=error_msg)


def lock(
    params: LockParams,
    rpc_url: str = SOLANA_MAINNET_RPC,
) -> LockResult:
    return asyncio.run(lock_async(params, rpc_url))
