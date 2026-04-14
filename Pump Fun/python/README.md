# jellychain-pumpfun-sdk

> **JellyChain SDK** for launching, buying back, locking, and claiming fees on [Pump.fun](https://pump.fun) (Solana) — Python edition

[![PyPI version](https://img.shields.io/pypi/v/jellychain-pumpfun-sdk)](https://pypi.org/project/jellychain-pumpfun-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

| Resource | Link |
|---|---|
| Docs | [jellychain.fun/docs](https://jellychain.fun/docs) |
| Terminal | [terminal.jellychain.fun](https://terminal.jellychain.fun) |
| GitHub | [github.com/jelly-chain](https://github.com/jelly-chain) |

---

## Features

- **Launch** — Deploy a new token on Pump.fun with full metadata, IPFS upload, and optional dev-buy
- **Buyback** — Purchase tokens from the bonding curve with a specified SOL amount
- **Lock** — Renounce/burn dev token allocation to signal commitment (no rug)
- **Claim Fees** — Collect and distribute accumulated Pump.fun creator fees

Both synchronous and `async/await` APIs are available.

---

## Installation

```bash
pip install jellychain-pumpfun-sdk
```

---

## Quick Start

```python
from jellychain_pumpfun import JellychainPumpFunSDK

sdk = JellychainPumpFunSDK(
    rpc_url="https://api.mainnet-beta.solana.com",
    pump_portal_api_key="YOUR_PUMP_PORTAL_API_KEY",
    slippage_bps=1500,
    priority_fee_sol=0.00005,
)

wallet = sdk.wallet_from_base58("YOUR_BASE58_PRIVATE_KEY")
print(sdk.docs_url)      # https://jellychain.fun/docs
print(sdk.terminal_url)  # https://terminal.jellychain.fun
```

---

## Usage

### Launch a Token

```python
from jellychain_pumpfun import JellychainPumpFunSDK, LaunchParams, TokenMetadata

sdk = JellychainPumpFunSDK(pump_portal_api_key="YOUR_API_KEY")

result = sdk.launch(LaunchParams(
    private_key_base58="YOUR_PRIVATE_KEY",
    metadata=TokenMetadata(
        name="Jelly Token",
        symbol="JELLY",
        description="The JellyChain memecoin",
        image_url="https://example.com/image.png",
        twitter="https://twitter.com/jellychain",
        telegram="https://t.me/jellychain",
        website="https://jellychain.fun",
    ),
    dev_buy_amount_sol=0.1,
))

if result.success:
    print(f"Mint: {result.mint_address}")
    print(f"TX:   {result.launch_tx_signature}")
    print(f"URL:  {result.pumpfun_url}")
```

### Buyback

```python
from jellychain_pumpfun import JellychainPumpFunSDK, BuybackParams

sdk = JellychainPumpFunSDK(pump_portal_api_key="YOUR_API_KEY")

result = sdk.buyback(BuybackParams(
    private_key_base58="YOUR_PRIVATE_KEY",
    mint_address="YOUR_MINT_ADDRESS",
    sol_amount=0.5,
    pool="pump",
    slippage_bps=2000,
))

if result.success:
    print(f"Buyback TX: {result.tx_signature}")
```

### Lock Dev Tokens (Burn / Renounce)

```python
from jellychain_pumpfun import JellychainPumpFunSDK, LockParams

sdk = JellychainPumpFunSDK()

result = sdk.lock(LockParams(
    private_key_base58="YOUR_PRIVATE_KEY",
    mint_address="YOUR_MINT_ADDRESS",
    lock_type="burn",   # 'burn' | 'renounce'
))

if result.success:
    print(f"Locked {result.locked_amount} tokens")
    print(f"TX: {result.tx_signature}")
```

### Claim Creator Fees

```python
from jellychain_pumpfun import JellychainPumpFunSDK, ClaimFeesParams

sdk = JellychainPumpFunSDK(pump_portal_api_key="YOUR_API_KEY")

result = sdk.claim_fees(ClaimFeesParams(
    private_key_base58="YOUR_PRIVATE_KEY",
    recipient_address="RECIPIENT_WALLET_ADDRESS",   # optional
))

if result.success:
    print(f"Claimed: {result.total_claimed_sol} SOL")
    print(f"TX: {result.claim_tx_signature}")
```

---

## Async API

All functions have `_async` variants for use in async contexts:

```python
import asyncio
from jellychain_pumpfun import launch_async, LaunchParams, TokenMetadata

async def main():
    result = await launch_async(
        LaunchParams(
            private_key_base58="YOUR_PRIVATE_KEY",
            metadata=TokenMetadata(
                name="Jelly Token",
                symbol="JELLY",
                description="The JellyChain memecoin",
                image_url="https://example.com/image.png",
            ),
        ),
        pump_portal_api_key="YOUR_API_KEY",
    )
    print(result)

asyncio.run(main())
```

---

## Wallet Utilities

```python
from jellychain_pumpfun import JellychainWallet

wallet = JellychainWallet.generate()
wallet2 = JellychainWallet.from_base58("your-base58-private-key")
private_key = wallet.to_base58_private_key()
print(wallet.public_key)
```

---

## Constants

```python
from jellychain_pumpfun import (
    PUMPFUN_PROGRAM_ID,
    PUMPFUN_GLOBAL_ACCOUNT,
    BURN_ADDRESS,
    TOTAL_SUPPLY,
    LAMPORTS_PER_SOL,
    JELLYCHAIN_DOCS_URL,
    JELLYCHAIN_TERMINAL_URL,
)
```

---

## Environment Variables

```env
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
PRIVATE_KEY_BASE58=your-wallet-private-key-in-base58
PUMP_PORTAL_API_KEY=your-pumpportal-api-key
MINT_ADDRESS=your-token-mint-address
RECIPIENT_ADDRESS=fee-recipient-wallet
```

---

## Examples

See the [`examples/`](./examples) directory for full runnable scripts:

- `examples/launch.py` — Launch a token
- `examples/buyback.py` — Execute a buyback
- `examples/lock.py` — Lock dev tokens
- `examples/claim_fees.py` — Claim creator fees

---

## License

MIT — built with love by [JellyChain](https://jellychain.fun)
