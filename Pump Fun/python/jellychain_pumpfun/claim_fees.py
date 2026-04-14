from __future__ import annotations
import asyncio
import json
import os
from solders.pubkey import Pubkey
from solders.system_program import ID as SYSTEM_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address
from anchorpy import Program, Provider, Wallet
from anchorpy.idl import Idl
from solana.rpc.commitment import Confirmed

from .constants import (
    PUMPFUN_PROGRAM_ID,
    PUMPFUN_GLOBAL_ACCOUNT,
    PUMPFUN_EVENT_AUTHORITY,
    CREATOR_VAULT_SEED,
    BONDING_CURVE_SEED,
    SOLSCAN_TX_URL,
    SOLANA_MAINNET_RPC,
    LAMPORTS_PER_SOL,
)
from .types import ClaimFeesParams, ClaimFeesResult
from .wallet import JellychainWallet, create_async_client

_IDL_PATH = os.path.join(os.path.dirname(__file__), "pumpfun_idl.json")


def load_idl() -> dict:
    with open(_IDL_PATH, "r") as f:
        return json.load(f)


def derive_creator_vault_pda(
    mint: Pubkey,
    creator: Pubkey,
) -> tuple[Pubkey, int]:
    return Pubkey.find_program_address(
        [CREATOR_VAULT_SEED, bytes(mint), bytes(creator)],
        PUMPFUN_PROGRAM_ID,
    )


def derive_bonding_curve_pda(mint: Pubkey) -> tuple[Pubkey, int]:
    return Pubkey.find_program_address(
        [BONDING_CURVE_SEED, bytes(mint)],
        PUMPFUN_PROGRAM_ID,
    )


async def claim_fees_async(
    params: ClaimFeesParams,
    rpc_url: str = SOLANA_MAINNET_RPC,
) -> ClaimFeesResult:
    if not params.mint_address:
        return ClaimFeesResult(
            success=False,
            error="mint_address is required for on-chain fee claim via Anchor",
        )

    try:
        wallet = JellychainWallet.from_base58(params.private_key_base58)
        mint = Pubkey.from_string(params.mint_address)

        idl_dict = load_idl()
        idl = Idl.from_json(json.dumps(idl_dict))

        bonding_curve, _ = derive_bonding_curve_pda(mint)
        creator_vault, _ = derive_creator_vault_pda(mint, wallet.public_key)

        associated_bonding_curve = get_associated_token_address(bonding_curve, mint)
        associated_user = get_associated_token_address(wallet.public_key, mint)

        print(f"[JellyChain] Claiming fees for mint: {params.mint_address}")
        print(f"[JellyChain] Bonding curve:   {bonding_curve}")
        print(f"[JellyChain] Creator vault:   {creator_vault}")

        async with create_async_client(rpc_url) as client:
            vault_balance_resp = await client.get_balance(creator_vault, commitment=Confirmed)
            vault_balance = vault_balance_resp.value

        if vault_balance == 0:
            return ClaimFeesResult(
                success=True,
                total_claimed_sol=0.0,
                error="Creator vault is empty — no fees to claim",
            )

        print(f"[JellyChain] Creator vault balance: {vault_balance / LAMPORTS_PER_SOL} SOL")

        async with create_async_client(rpc_url) as client:
            anchor_wallet = Wallet(wallet.keypair)
            provider = Provider(client, anchor_wallet)
            program = Program(idl, PUMPFUN_PROGRAM_ID, provider)

            accounts = {
                "global": PUMPFUN_GLOBAL_ACCOUNT,
                "mint": mint,
                "bonding_curve": bonding_curve,
                "associated_bonding_curve": associated_bonding_curve,
                "creator_vault": creator_vault,
                "creator": wallet.public_key,
                "associated_user": associated_user,
                "system_program": SYSTEM_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
                "event_authority": PUMPFUN_EVENT_AUTHORITY,
                "program": PUMPFUN_PROGRAM_ID,
            }

            tx_sig = await program.rpc["withdraw"](
                ctx=program.ctx(accounts=accounts),
            )

        print(f"[JellyChain] Creator fees claimed: TX={tx_sig}")

        return ClaimFeesResult(
            success=True,
            claim_tx_signature=str(tx_sig),
            total_claimed_sol=vault_balance / LAMPORTS_PER_SOL,
            solscan_url=f"{SOLSCAN_TX_URL}/{tx_sig}",
        )

    except Exception as exc:
        error_msg = str(exc)
        print(f"[JellyChain] Claim fees failed: {error_msg}")
        return ClaimFeesResult(success=False, error=error_msg)


async def get_creator_vault_balance_async(
    mint_address: str,
    creator_address: str,
    rpc_url: str = SOLANA_MAINNET_RPC,
) -> float:
    mint = Pubkey.from_string(mint_address)
    creator = Pubkey.from_string(creator_address)
    vault_pda, _ = derive_creator_vault_pda(mint, creator)

    async with create_async_client(rpc_url) as client:
        resp = await client.get_balance(vault_pda)
        return resp.value / LAMPORTS_PER_SOL


def get_creator_vault_balance(
    mint_address: str,
    creator_address: str,
    rpc_url: str = SOLANA_MAINNET_RPC,
) -> float:
    return asyncio.run(get_creator_vault_balance_async(mint_address, creator_address, rpc_url))


def claim_fees(
    params: ClaimFeesParams,
    rpc_url: str = SOLANA_MAINNET_RPC,
) -> ClaimFeesResult:
    return asyncio.run(claim_fees_async(params, rpc_url))
