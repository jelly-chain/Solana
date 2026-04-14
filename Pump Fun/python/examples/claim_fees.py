"""
Example: Claim Pump.fun creator fees using JellyChain Python SDK

Uses the Pump.fun program's withdraw instruction via anchorpy.
Creator fees accumulate in a per-mint PDA: [b"creator-vault", mint, creator].

Docs:     https://jellychain.fun/docs
Terminal: https://terminal.jellychain.fun
GitHub:   https://github.com/jelly-chain
"""
import os
from jellychain_pumpfun import (
    JellychainPumpFunSDK,
    ClaimFeesParams,
    get_creator_vault_balance,
)


def main() -> None:
    sdk = JellychainPumpFunSDK(
        rpc_url=os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
    )

    private_key = os.environ["PRIVATE_KEY_BASE58"]
    mint_address = os.environ["MINT_ADDRESS"]

    wallet = sdk.wallet_from_base58(private_key)
    print(f"[JellyChain] Claiming creator fees...")
    print(f"  Wallet: {wallet.public_key}")
    print(f"  Mint:   {mint_address}")

    vault_balance = get_creator_vault_balance(mint_address, str(wallet.public_key))
    print(f"  Creator vault balance: {vault_balance} SOL")

    result = sdk.claim_fees(ClaimFeesParams(
        private_key_base58=private_key,
        mint_address=mint_address,
    ))

    if result.success:
        print("Fees claimed!")
        print(f"  Total claimed: {result.total_claimed_sol} SOL")
        print(f"  Claim TX:      {result.claim_tx_signature}")
        print(f"  Solscan:       {result.solscan_url}")
    else:
        print(f"Claim failed: {result.error}")


if __name__ == "__main__":
    main()
