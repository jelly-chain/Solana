# @jellychain/pumpfun-sdk

> **JellyChain SDK** for launching, buying back, locking, and claiming fees on [Pump.fun](https://pump.fun) (Solana)

[![npm version](https://img.shields.io/npm/v/@jellychain/pumpfun-sdk)](https://www.npmjs.com/package/@jellychain/pumpfun-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

Supports both the **PumpPortal Lightning API** (fastest) and **direct on-chain Anchor transactions**.

---

## Installation

```bash
npm install @jellychain/pumpfun-sdk
# or
yarn add @jellychain/pumpfun-sdk
# or
pnpm add @jellychain/pumpfun-sdk
```

---

## Quick Start

```typescript
import { JellychainPumpFunSDK, JellychainWallet } from '@jellychain/pumpfun-sdk';

const sdk = new JellychainPumpFunSDK({
  rpcUrl: 'https://api.mainnet-beta.solana.com',
  pumpPortalApiKey: 'YOUR_PUMP_PORTAL_API_KEY',
  slippageBps: 1500,     // 15% slippage
  priorityFeeSol: 0.00005,
});

const wallet = sdk.walletFromBase58(process.env.PRIVATE_KEY_BASE58!);
```

---

## Usage

### Launch a Token

```typescript
const result = await sdk.launch({
  wallet: wallet.payer,
  metadata: {
    name: 'Jelly Token',
    symbol: 'JELLY',
    description: 'The JellyChain memecoin',
    imageUrl: 'https://example.com/image.png',
    twitter: 'https://twitter.com/jellychain',
    telegram: 'https://t.me/jellychain',
    website: 'https://jellychain.fun',
  },
  devBuyAmountSol: 0.1,   // optional dev buy
});

if (result.success) {
  console.log('Mint:', result.mintAddress);
  console.log('TX:', result.launchTxSignature);
  console.log('Pump.fun:', result.pumpfunUrl);
}
```

### Buyback

```typescript
const result = await sdk.buyback({
  wallet: wallet.payer,
  mintAddress: 'YOUR_MINT_ADDRESS',
  solAmount: 0.5,
  pool: 'pump',       // 'pump' | 'raydium'
  slippageBps: 2000,  // 20% slippage
});

if (result.success) {
  console.log('Buyback TX:', result.txSignature);
}
```

### Lock Dev Tokens (Renounce / Burn)

```typescript
const result = await sdk.lock({
  wallet: wallet.payer,
  mintAddress: 'YOUR_MINT_ADDRESS',
  lockType: 'burn',   // 'burn' | 'renounce'
});

if (result.success) {
  console.log('Locked:', result.lockedAmount, 'tokens');
  console.log('TX:', result.txSignature);
}
```

### Claim Creator Fees

```typescript
const result = await sdk.claimFees({
  wallet: wallet.payer,
  recipientAddress: 'RECIPIENT_WALLET_ADDRESS',  // optional, defaults to wallet
});

if (result.success) {
  console.log('Claimed:', result.totalClaimedSol, 'SOL');
  console.log('Claim TX:', result.claimTxSignature);
}
```

---

## Standalone Functions

All SDK methods are also available as standalone exported functions:

```typescript
import {
  launch,
  buyback,
  lock,
  claimFees,
  JellychainWallet,
  createPumpPortalWallet,
  deriveCreatorVaultPDA,
} from '@jellychain/pumpfun-sdk';
```

---

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `rpcUrl` | `string` | Solana mainnet | Solana RPC endpoint URL |
| `commitment` | `Commitment` | `'confirmed'` | Transaction commitment level |
| `pumpPortalApiKey` | `string` | — | PumpPortal API key for Lightning mode |
| `priorityFeeSol` | `number` | `0.00005` | Priority fee in SOL |
| `slippageBps` | `number` | `1500` | Slippage in basis points (1500 = 15%) |

---

## Constants

```typescript
import {
  PUMPFUN_PROGRAM_ID,
  PUMPFUN_GLOBAL_ACCOUNT,
  PUMPFUN_FEE_RECIPIENT,
  TOTAL_SUPPLY,
  BURN_ADDRESS,
} from '@jellychain/pumpfun-sdk';
```

---

## Wallet Utilities

```typescript
import { JellychainWallet } from '@jellychain/pumpfun-sdk';

const wallet = JellychainWallet.generate();
const wallet2 = JellychainWallet.fromBase58('your-base58-private-key');
const privateKey = wallet.toBase58PrivateKey();
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

- `examples/launch.ts` — Launch a token
- `examples/buyback.ts` — Execute a buyback
- `examples/lock.ts` — Lock dev tokens
- `examples/claimFees.ts` — Claim creator fees

---

## License

MIT — built with love by [JellyChain](https://jellychain.fun)
