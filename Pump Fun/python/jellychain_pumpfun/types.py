from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TokenMetadata:
    name: str
    symbol: str
    description: str
    image_url: str
    website: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None


@dataclass
class LaunchParams:
    private_key_base58: str
    metadata: TokenMetadata
    dev_buy_amount_sol: float = 0.0
    slippage_bps: int = 1500
    priority_fee_sol: float = 0.00005


@dataclass
class LaunchResult:
    success: bool
    mint_address: Optional[str] = None
    mint_private_key_base58: Optional[str] = None
    launch_tx_signature: Optional[str] = None
    dev_buy_tx_signature: Optional[str] = None
    metadata_uri: Optional[str] = None
    solscan_url: Optional[str] = None
    pumpfun_url: Optional[str] = None
    error: Optional[str] = None


@dataclass
class BuybackParams:
    private_key_base58: str
    mint_address: str
    sol_amount: float
    slippage_bps: int = 1500
    priority_fee_sol: float = 0.00005
    pool: str = "pump"


@dataclass
class BuybackResult:
    success: bool
    tx_signature: Optional[str] = None
    solscan_url: Optional[str] = None
    error: Optional[str] = None


@dataclass
class LockParams:
    private_key_base58: str
    mint_address: str
    lock_type: str = "burn"
    amount_tokens: Optional[int] = None
    priority_fee_sol: float = 0.00005


@dataclass
class LockResult:
    success: bool
    tx_signature: Optional[str] = None
    solscan_url: Optional[str] = None
    locked_amount: Optional[str] = None
    lock_type: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ClaimFeesParams:
    private_key_base58: str
    mint_address: Optional[str] = None
    priority_fee_sol: float = 0.00005
    recipient_address: Optional[str] = None


@dataclass
class ClaimFeesResult:
    success: bool
    claim_tx_signature: Optional[str] = None
    distribute_tx_signature: Optional[str] = None
    total_claimed_sol: Optional[float] = None
    solscan_url: Optional[str] = None
    error: Optional[str] = None


@dataclass
class PumpPortalWallet:
    wallet_public_key: str
    private_key: str
    api_key: str
