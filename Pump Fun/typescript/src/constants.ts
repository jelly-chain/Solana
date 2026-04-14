import { PublicKey } from '@solana/web3.js';

export const PUMPFUN_PROGRAM_ID = new PublicKey('6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P');

export const PUMPFUN_GLOBAL_ACCOUNT = new PublicKey('4wTV81ckZkh8rFZqAaQFQFT1aYhZXxTnZGF4JsNjZxo');

export const PUMPFUN_FEE_RECIPIENT = new PublicKey('CebN5WGQ4jvEPvsVU4EoHEpgznyQHeU2bydX8sDfANLE');

export const PUMPFUN_MPL_TOKEN_METADATA = new PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s');

export const PUMPFUN_EVENT_AUTHORITY = new PublicKey('Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1');

export const PUMPFUN_MINT_AUTHORITY = new PublicKey('TSLvdd1pWpHVjahSpsvCXUbgwsL3Ao3sksFXZFeeCip');

export const TOKEN_DECIMALS = 6;

export const TOTAL_SUPPLY = 1_000_000_000;

export const SOL_DECIMALS = 9;

export const LAMPORTS_PER_SOL = 1_000_000_000;

export const PUMPPORTAL_BASE_URL = 'https://pumpportal.fun/api';
export const PUMPPORTAL_TRADE_URL = `${PUMPPORTAL_BASE_URL}/trade`;
export const PUMPPORTAL_CREATE_WALLET_URL = `${PUMPPORTAL_BASE_URL}/create-wallet`;
export const PUMPPORTAL_IPFS_URL = `${PUMPPORTAL_BASE_URL}/ipfs`;

export const SOLANA_MAINNET_RPC = 'https://api.mainnet-beta.solana.com';
export const SOLANA_DEVNET_RPC = 'https://api.devnet.solana.com';

export const JELLYCHAIN_DOCS_URL = 'https://jellychain.fun/docs';
export const JELLYCHAIN_TERMINAL_URL = 'https://terminal.jellychain.fun';
export const JELLYCHAIN_GITHUB_URL = 'https://github.com/jelly-chain';

export const SOLSCAN_TX_URL = 'https://solscan.io/tx';
export const SOLSCAN_TOKEN_URL = 'https://solscan.io/token';
export const PUMPFUN_TOKEN_URL = 'https://pump.fun';

export const DEFAULT_SLIPPAGE_BPS = 1500;
export const DEFAULT_PRIORITY_FEE_SOL = 0.00005;
export const DEFAULT_COMMITMENT = 'confirmed' as const;

export const LOCK_PROGRAM_SEED = 'lock';
export const BONDING_CURVE_SEED = 'bonding-curve';
export const CREATOR_VAULT_SEED = 'creator-vault';

export const BURN_ADDRESS = new PublicKey('1nc1nerator11111111111111111111111111111111');
