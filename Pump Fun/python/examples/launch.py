"""
Example: Launch a token on Pump.fun using JellyChain Python SDK

Docs:     https://jellychain.fun/docs
Terminal: https://terminal.jellychain.fun
GitHub:   https://github.com/jelly-chain
"""
import os
from jellychain_pumpfun import (
    JellychainPumpFunSDK,
    LaunchParams,
    TokenMetadata,
)


def main() -> None:
    sdk = JellychainPumpFunSDK(
        rpc_url=os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
        pump_portal_api_key=os.getenv("PUMP_PORTAL_API_KEY", ""),
        slippage_bps=1500,
        priority_fee_sol=0.00005,
    )

    wallet = sdk.create_wallet() if not os.getenv("PRIVATE_KEY_BASE58") else sdk.wallet_from_base58(os.environ["PRIVATE_KEY_BASE58"])
    print(f"Wallet: {wallet.public_key}")
    print(f"Docs:   {sdk.docs_url}")

    result = sdk.launch(LaunchParams(
        private_key_base58=wallet.to_base58_private_key(),
        metadata=TokenMetadata(
            name="Jelly Token",
            symbol="JELLY",
            description="The official JellyChain memecoin — powered by https://jellychain.fun",
            image_url="https://picsum.photos/500/500",
            twitter="https://twitter.com/jellychain",
            telegram="https://t.me/jellychain",
            website="https://jellychain.fun",
        ),
        dev_buy_amount_sol=0.1,
    ))

    if result.success:
        print("Token launched!")
        print(f"  Mint:    {result.mint_address}")
        print(f"  TX:      {result.launch_tx_signature}")
        print(f"  Solscan: {result.solscan_url}")
        print(f"  Pump.fun:{result.pumpfun_url}")
    else:
        print(f"Launch failed: {result.error}")


if __name__ == "__main__":
    main()
