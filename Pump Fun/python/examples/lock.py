"""
Example: Lock (burn) dev tokens on Pump.fun using JellyChain Python SDK

Docs:     https://jellychain.fun/docs
Terminal: https://terminal.jellychain.fun
GitHub:   https://github.com/jelly-chain
"""
import os
from jellychain_pumpfun import JellychainPumpFunSDK, LockParams


def main() -> None:
    sdk = JellychainPumpFunSDK(
        rpc_url=os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
    )

    private_key = os.environ["PRIVATE_KEY_BASE58"]
    mint_address = os.environ["MINT_ADDRESS"]

    wallet = sdk.wallet_from_base58(private_key)
    print(f"[JellyChain] Locking dev tokens...")
    print(f"  Wallet: {wallet.public_key}")
    print(f"  Mint:   {mint_address}")

    result = sdk.lock(LockParams(
        private_key_base58=private_key,
        mint_address=mint_address,
        lock_type="burn",
    ))

    if result.success:
        print("Tokens locked!")
        print(f"  Locked amount: {result.locked_amount}")
        print(f"  Lock type:     {result.lock_type}")
        print(f"  TX:            {result.tx_signature}")
        print(f"  Solscan:       {result.solscan_url}")
    else:
        print(f"Lock failed: {result.error}")


if __name__ == "__main__":
    main()
