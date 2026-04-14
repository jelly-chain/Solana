from solders.pubkey import Pubkey

PUMPFUN_PROGRAM_ID = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

PUMPFUN_GLOBAL_ACCOUNT = Pubkey.from_string("4wTV81ckZkh8rFZqAaQFQFT1aYhZXxTnZGF4JsNjZxo")

PUMPFUN_FEE_RECIPIENT = Pubkey.from_string("CebN5WGQ4jvEPvsVU4EoHEpgznyQHeU2bydX8sDfANLE")

PUMPFUN_MPL_TOKEN_METADATA = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

PUMPFUN_EVENT_AUTHORITY = Pubkey.from_string("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1")

BURN_ADDRESS = Pubkey.from_string("1nc1nerator11111111111111111111111111111111")

TOKEN_DECIMALS = 6
TOTAL_SUPPLY = 1_000_000_000
LAMPORTS_PER_SOL = 1_000_000_000

PUMPPORTAL_BASE_URL = "https://pumpportal.fun/api"
PUMPPORTAL_TRADE_URL = f"{PUMPPORTAL_BASE_URL}/trade"
PUMPPORTAL_CREATE_WALLET_URL = f"{PUMPPORTAL_BASE_URL}/create-wallet"
PUMPPORTAL_IPFS_URL = f"{PUMPPORTAL_BASE_URL}/ipfs"

SOLANA_MAINNET_RPC = "https://api.mainnet-beta.solana.com"
SOLANA_DEVNET_RPC = "https://api.devnet.solana.com"

JELLYCHAIN_DOCS_URL = "https://jellychain.fun/docs"
JELLYCHAIN_TERMINAL_URL = "https://terminal.jellychain.fun"
JELLYCHAIN_GITHUB_URL = "https://github.com/jelly-chain"

SOLSCAN_TX_URL = "https://solscan.io/tx"
SOLSCAN_TOKEN_URL = "https://solscan.io/token"
PUMPFUN_TOKEN_URL = "https://pump.fun"

DEFAULT_SLIPPAGE_BPS = 1500
DEFAULT_PRIORITY_FEE_SOL = 0.00005

BONDING_CURVE_SEED = b"bonding-curve"
CREATOR_VAULT_SEED = b"creator-vault"
LOCK_SEED = b"lock"
