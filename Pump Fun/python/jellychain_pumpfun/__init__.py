"""
JellyChain Pump.fun SDK for Solana

Launch, buyback, lock, and claim fees on Pump.fun using Python.

Docs:     https://jellychain.fun/docs
Terminal: https://terminal.jellychain.fun
GitHub:   https://github.com/jelly-chain
"""
from .constants import (
    PUMPFUN_PROGRAM_ID,
    PUMPFUN_GLOBAL_ACCOUNT,
    PUMPFUN_FEE_RECIPIENT,
    BURN_ADDRESS,
    TOTAL_SUPPLY,
    TOKEN_DECIMALS,
    LAMPORTS_PER_SOL,
    SOLANA_MAINNET_RPC,
    SOLANA_DEVNET_RPC,
    JELLYCHAIN_DOCS_URL,
    JELLYCHAIN_TERMINAL_URL,
    JELLYCHAIN_GITHUB_URL,
    DEFAULT_SLIPPAGE_BPS,
    DEFAULT_PRIORITY_FEE_SOL,
)
from .types import (
    TokenMetadata,
    LaunchParams,
    LaunchResult,
    BuybackParams,
    BuybackResult,
    LockParams,
    LockResult,
    ClaimFeesParams,
    ClaimFeesResult,
    PumpPortalWallet,
)
from .wallet import JellychainWallet, create_client, create_async_client
from .launch import (
    launch,
    launch_async,
    create_pumpportal_wallet,
    upload_metadata_to_pumpportal,
)
from .buyback import buyback, buyback_async
from .lock import lock, lock_async
from .claim_fees import (
    claim_fees,
    claim_fees_async,
    derive_creator_vault_pda,
    derive_bonding_curve_pda,
    get_creator_vault_balance,
    get_creator_vault_balance_async,
    load_idl,
)

__version__ = "1.0.0"
__author__ = "JellyChain"
__license__ = "MIT"

DOCS_URL = JELLYCHAIN_DOCS_URL
TERMINAL_URL = JELLYCHAIN_TERMINAL_URL


class JellychainPumpFunSDK:
    """
    JellyChain Pump.fun SDK

    A high-level interface for interacting with Pump.fun on Solana.

    Usage::

        from jellychain_pumpfun import JellychainPumpFunSDK, TokenMetadata, LaunchParams

        sdk = JellychainPumpFunSDK(
            rpc_url="https://api.mainnet-beta.solana.com",
            pump_portal_api_key="YOUR_API_KEY",
        )

        result = sdk.launch(LaunchParams(
            private_key_base58="YOUR_PRIVATE_KEY",
            metadata=TokenMetadata(
                name="Jelly Token",
                symbol="JELLY",
                description="The JellyChain memecoin",
                image_url="https://example.com/image.png",
            ),
            dev_buy_amount_sol=0.1,
        ))
    """

    def __init__(
        self,
        rpc_url: str = SOLANA_MAINNET_RPC,
        pump_portal_api_key: str = "",
        slippage_bps: int = DEFAULT_SLIPPAGE_BPS,
        priority_fee_sol: float = DEFAULT_PRIORITY_FEE_SOL,
    ) -> None:
        self.rpc_url = rpc_url
        self.pump_portal_api_key = pump_portal_api_key
        self.slippage_bps = slippage_bps
        self.priority_fee_sol = priority_fee_sol
        self.docs_url = JELLYCHAIN_DOCS_URL
        self.terminal_url = JELLYCHAIN_TERMINAL_URL

    @property
    def idl(self) -> dict:
        return load_idl()

    def launch(self, params: LaunchParams) -> LaunchResult:
        if params.slippage_bps == DEFAULT_SLIPPAGE_BPS:
            params.slippage_bps = self.slippage_bps
        if params.priority_fee_sol == DEFAULT_PRIORITY_FEE_SOL:
            params.priority_fee_sol = self.priority_fee_sol
        return launch(params, self.pump_portal_api_key or None)

    def buyback(self, params: BuybackParams) -> BuybackResult:
        if not self.pump_portal_api_key:
            raise ValueError("pump_portal_api_key is required for buyback via PumpPortal")
        if params.slippage_bps == DEFAULT_SLIPPAGE_BPS:
            params.slippage_bps = self.slippage_bps
        if params.priority_fee_sol == DEFAULT_PRIORITY_FEE_SOL:
            params.priority_fee_sol = self.priority_fee_sol
        return buyback(params, self.pump_portal_api_key)

    def lock(self, params: LockParams) -> LockResult:
        return lock(params, self.rpc_url)

    def claim_fees(self, params: ClaimFeesParams) -> ClaimFeesResult:
        return claim_fees(params, self.rpc_url)

    def get_creator_vault_balance(
        self,
        mint_address: str,
        creator_address: str,
    ) -> float:
        return get_creator_vault_balance(mint_address, creator_address, self.rpc_url)

    def create_wallet(self) -> JellychainWallet:
        return JellychainWallet.generate()

    def wallet_from_base58(self, private_key: str) -> JellychainWallet:
        return JellychainWallet.from_base58(private_key)


__all__ = [
    "JellychainPumpFunSDK",
    "JellychainWallet",
    "TokenMetadata",
    "LaunchParams",
    "LaunchResult",
    "BuybackParams",
    "BuybackResult",
    "LockParams",
    "LockResult",
    "ClaimFeesParams",
    "ClaimFeesResult",
    "PumpPortalWallet",
    "launch",
    "launch_async",
    "buyback",
    "buyback_async",
    "lock",
    "lock_async",
    "claim_fees",
    "claim_fees_async",
    "create_pumpportal_wallet",
    "upload_metadata_to_pumpportal",
    "derive_creator_vault_pda",
    "derive_bonding_curve_pda",
    "get_creator_vault_balance",
    "get_creator_vault_balance_async",
    "load_idl",
    "create_client",
    "create_async_client",
    "PUMPFUN_PROGRAM_ID",
    "PUMPFUN_GLOBAL_ACCOUNT",
    "PUMPFUN_FEE_RECIPIENT",
    "BURN_ADDRESS",
    "TOTAL_SUPPLY",
    "TOKEN_DECIMALS",
    "LAMPORTS_PER_SOL",
    "SOLANA_MAINNET_RPC",
    "SOLANA_DEVNET_RPC",
    "JELLYCHAIN_DOCS_URL",
    "JELLYCHAIN_TERMINAL_URL",
    "DOCS_URL",
    "TERMINAL_URL",
    "__version__",
]
