# JellyChain Pump.fun SDK — Solana

> Standalone SDKs for interacting with [Pump.fun](https://pump.fun) on Solana

| Resource | Link |
|---|---|
| Docs | [jellychain.fun/docs](https://jellychain.fun/docs) |
| Terminal | [terminal.jellychain.fun](https://terminal.jellychain.fun) |
| GitHub | [github.com/jelly-chain](https://github.com/jelly-chain) |

---

## Packages

| Language | Package | Directory |
|---|---|---|
| TypeScript / Node.js | `@jellychain/pumpfun-sdk` | [`typescript/`](./typescript) |
| Python | `jellychain-pumpfun-sdk` | [`python/`](./python) |

---

## Capabilities

Both SDKs expose the same four core actions:

| Action | Description |
|---|---|
| **launch** | Deploy a new Pump.fun token with metadata, IPFS upload, and optional dev-buy |
| **buyback** | Buy tokens from the bonding curve with a specified SOL amount |
| **lock** | Burn/renounce dev token allocation to signal long-term commitment |
| **claimFees** | Collect and distribute accumulated Pump.fun creator fees |

---

## Quick links

- TypeScript README: [`typescript/README.md`](./typescript/README.md)
- Python README: [`python/README.md`](./python/README.md)
