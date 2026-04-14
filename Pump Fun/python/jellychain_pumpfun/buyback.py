from __future__ import annotations
import asyncio
import httpx
from solders.keypair import Keypair

from .constants import (
    PUMPPORTAL_TRADE_URL,
    SOLSCAN_TX_URL,
    LAMPORTS_PER_SOL,
    DEFAULT_SLIPPAGE_BPS,
    DEFAULT_PRIORITY_FEE_SOL,
)
from .types import BuybackParams, BuybackResult


async def _call_pumpportal(api_key: str, payload: dict) -> dict:
    url = f"{PUMPPORTAL_TRADE_URL}?api-key={api_key}"
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    if data.get("error"):
        raise RuntimeError(f"PumpPortal error: {data['error']}")
    if not data.get("signature"):
        raise RuntimeError("PumpPortal returned no signature")

    return data


async def buyback_async(
    params: BuybackParams,
    pump_portal_api_key: str,
) -> BuybackResult:
    slippage = params.slippage_bps // 100
    try:
        print(f"[JellyChain] Buyback: {params.sol_amount} SOL -> {params.mint_address}")

        payload = {
            "action": "buy",
            "mint": params.mint_address,
            "amount": params.sol_amount,
            "denominatedInSol": "true",
            "slippage": slippage,
            "priorityFee": params.priority_fee_sol,
            "pool": params.pool,
        }

        result = await _call_pumpportal(pump_portal_api_key, payload)
        tx_sig = result["signature"]

        print(f"[JellyChain] Buyback successful: TX={tx_sig}")

        return BuybackResult(
            success=True,
            tx_signature=tx_sig,
            solscan_url=f"{SOLSCAN_TX_URL}/{tx_sig}",
        )

    except Exception as exc:
        error_msg = str(exc)
        print(f"[JellyChain] Buyback failed: {error_msg}")
        return BuybackResult(success=False, error=error_msg)


def buyback(
    params: BuybackParams,
    pump_portal_api_key: str,
) -> BuybackResult:
    return asyncio.run(buyback_async(params, pump_portal_api_key))
