from __future__ import annotations
import asyncio
import base64
import base58
import httpx
from solders.keypair import Keypair

from .constants import (
    PUMPPORTAL_IPFS_URL,
    PUMPPORTAL_TRADE_URL,
    PUMPPORTAL_CREATE_WALLET_URL,
    SOLSCAN_TX_URL,
    PUMPFUN_TOKEN_URL,
    DEFAULT_SLIPPAGE_BPS,
    DEFAULT_PRIORITY_FEE_SOL,
)
from .types import LaunchParams, LaunchResult, TokenMetadata, PumpPortalWallet


async def create_pumpportal_wallet() -> PumpPortalWallet:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(PUMPPORTAL_CREATE_WALLET_URL)
        response.raise_for_status()
        data = response.json()
        if not all(k in data for k in ("walletPublicKey", "privateKey", "apiKey")):
            raise ValueError(f"PumpPortal returned incomplete wallet data: {list(data.keys())}")
        return PumpPortalWallet(
            wallet_public_key=data["walletPublicKey"],
            private_key=data["privateKey"],
            api_key=data["apiKey"],
        )


async def upload_metadata_to_pumpportal(metadata: TokenMetadata) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        if metadata.image_url.startswith("data:"):
            header, b64_data = metadata.image_url.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]
            image_bytes = base64.b64decode(b64_data)
        else:
            img_response = await client.get(metadata.image_url)
            img_response.raise_for_status()
            image_bytes = img_response.content
            mime_type = img_response.headers.get("content-type", "image/png")

        files = {"file": ("token-image.png", image_bytes, mime_type)}
        form_data: dict[str, str] = {
            "name": metadata.name,
            "symbol": metadata.symbol,
            "description": metadata.description,
            "showName": "true",
        }
        if metadata.twitter:
            form_data["twitter"] = metadata.twitter
        if metadata.telegram:
            form_data["telegram"] = metadata.telegram
        if metadata.website:
            form_data["website"] = metadata.website

        response = await client.post(PUMPPORTAL_IPFS_URL, data=form_data, files=files)
        response.raise_for_status()
        result = response.json()

        if "metadataUri" not in result:
            raise ValueError(f"PumpPortal IPFS upload returned no metadataUri: {result}")

        return result["metadataUri"]


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


async def launch_async(
    params: LaunchParams,
    pump_portal_api_key: str | None = None,
) -> LaunchResult:
    try:
        api_key = pump_portal_api_key
        if not api_key:
            print("[JellyChain] Creating PumpPortal lightning wallet...")
            portal_wallet = await create_pumpportal_wallet()
            api_key = portal_wallet.api_key

        print("[JellyChain] Uploading metadata to IPFS via PumpPortal...")
        metadata_uri = await upload_metadata_to_pumpportal(params.metadata)
        print(f"[JellyChain] Metadata URI: {metadata_uri}")

        mint_keypair = Keypair()
        mint_address = str(mint_keypair.pubkey())
        mint_private_key_b58 = base58.b58encode(bytes(mint_keypair)).decode("utf-8")

        buy_amount = params.dev_buy_amount_sol if params.dev_buy_amount_sol > 0 else 0.0001
        slippage = params.slippage_bps // 100

        print(f"[JellyChain] Creating token {params.metadata.symbol} ({mint_address})...")

        create_payload = {
            "action": "create",
            "tokenMetadata": {
                "name": params.metadata.name,
                "symbol": params.metadata.symbol,
                "uri": metadata_uri,
            },
            "mint": mint_private_key_b58,
            "denominatedInSol": "true",
            "amount": buy_amount,
            "slippage": slippage,
            "priorityFee": params.priority_fee_sol,
            "pool": "pump",
        }

        create_result = await _call_pumpportal(api_key, create_payload)
        launch_tx = create_result["signature"]

        print(f"[JellyChain] Token launched! Mint: {mint_address}, TX: {launch_tx}")

        return LaunchResult(
            success=True,
            mint_address=mint_address,
            mint_private_key_base58=mint_private_key_b58,
            launch_tx_signature=launch_tx,
            dev_buy_tx_signature=launch_tx if params.dev_buy_amount_sol > 0 else None,
            metadata_uri=metadata_uri,
            solscan_url=f"{SOLSCAN_TX_URL}/{launch_tx}",
            pumpfun_url=f"{PUMPFUN_TOKEN_URL}/{mint_address}",
        )

    except Exception as exc:
        error_msg = str(exc)
        print(f"[JellyChain] Launch failed: {error_msg}")
        return LaunchResult(success=False, error=error_msg)


def launch(
    params: LaunchParams,
    pump_portal_api_key: str | None = None,
) -> LaunchResult:
    return asyncio.run(launch_async(params, pump_portal_api_key))
