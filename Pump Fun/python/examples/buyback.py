"""
Example: Execute a token buyback on Pump.fun using JellyChain Python SDK

Docs:     https://jellychain.fun/docs
Terminal: https://terminal.jellychain.fun
GitHub:   https://github.com/jelly-chain
"""
import os
from jellychain_pumpfun import JellychainPumpFunSDK, BuybackParams


def main() -> None:
    sdk = JellychainPumpFunSDK(
        rpc_url=os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
        pump_portal_api_key=os.environ["PUMP_PORTAL_API_KEY"],
        slippage_bps=2000,
    )

    private_key = os.environ["PRIVATE_KEY_BASE58"]
    mint_address = os.environ["MINT_ADDRESS"]

    wallet = sdk.wallet_from_base58(private_key)
    print(f"[JellyChain] Executing buyback...")
    print(f"  Wallet: {wallet.public_key}")
    print(f"  Mint:   {mint_address}")

    result = sdk.buyback(BuybackParams(
        private_key_base58=private_key,
        mint_address=mint_address,
        sol_amount=0.5,
        pool="pump",
    ))

    if result.success:
        print("Buyback successful!")
        print(f"  TX:      {result.tx_signature}")
        print(f"  Solscan: {result.solscan_url}")
    else:
        print(f"Buyback failed: {result.error}")


if __name__ == "__main__":
    main()
