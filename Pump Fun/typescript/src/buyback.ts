import { PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js';
import { PumpFunSDK } from 'pumpdotfun-sdk';
import {
  PUMPPORTAL_TRADE_URL,
  SOLSCAN_TX_URL,
  DEFAULT_SLIPPAGE_BPS,
  DEFAULT_PRIORITY_FEE_SOL,
} from './constants';
import type { BuybackParams, BuybackResult } from './types';
import { JellychainWallet, createAnchorProvider } from './wallet';

async function callPumpPortal(
  apiKey: string,
  payload: Record<string, unknown>,
): Promise<{ signature: string }> {
  const url = `${PUMPPORTAL_TRADE_URL}?api-key=${apiKey}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`PumpPortal API error (${response.status}): ${text}`);
  }

  const data = (await response.json()) as { signature: string; error?: string };
  if (data.error) throw new Error(`PumpPortal error: ${data.error}`);
  if (!data.signature) throw new Error('PumpPortal returned no signature');

  return data;
}

export async function buybackViaPortal(
  params: BuybackParams,
  pumpPortalApiKey: string,
): Promise<BuybackResult> {
  const {
    mintAddress,
    solAmount,
    pool = 'pump',
  } = params;
  const slippage = Math.floor((params.slippageBps ?? DEFAULT_SLIPPAGE_BPS) / 100);
  const priorityFee = params.priorityFeeSol ?? DEFAULT_PRIORITY_FEE_SOL;

  try {
    console.log(`[JellyChain] Executing buyback: ${solAmount} SOL -> ${mintAddress}`);

    const payload = {
      action: 'buy',
      mint: mintAddress,
      amount: solAmount,
      denominatedInSol: 'true',
      slippage,
      priorityFee,
      pool,
    };

    const result = await callPumpPortal(pumpPortalApiKey, payload);

    console.log(`[JellyChain] Buyback successful: TX=${result.signature}`);

    return {
      success: true,
      txSignature: result.signature,
      solscanUrl: `${SOLSCAN_TX_URL}/${result.signature}`,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error('[JellyChain] Buyback failed:', errorMessage);
    return { success: false, error: errorMessage };
  }
}

export async function buybackViaAnchor(
  params: BuybackParams,
  rpcUrl?: string,
): Promise<BuybackResult> {
  const { wallet, mintAddress, solAmount } = params;
  const slippageBps = params.slippageBps ?? DEFAULT_SLIPPAGE_BPS;

  try {
    console.log(`[JellyChain] Executing on-chain buyback via Anchor: ${solAmount} SOL -> ${mintAddress}`);

    const jellychainWallet = new JellychainWallet(wallet);
    const provider = createAnchorProvider(jellychainWallet, rpcUrl);
    const sdk = new PumpFunSDK(provider);

    const mint = new PublicKey(mintAddress);
    const lamports = BigInt(Math.floor(solAmount * LAMPORTS_PER_SOL));

    const buyResult = await sdk.buy(wallet, mint, lamports, BigInt(slippageBps), {
      unitLimit: 250_000,
      unitPrice: Math.floor((params.priorityFeeSol ?? DEFAULT_PRIORITY_FEE_SOL) * 1e9),
    });

    if (!buyResult.success || !buyResult.signature) {
      throw new Error(`PumpFun SDK buy failed: ${JSON.stringify(buyResult)}`);
    }

    console.log(`[JellyChain] On-chain buyback successful: TX=${buyResult.signature}`);

    return {
      success: true,
      txSignature: buyResult.signature,
      solscanUrl: `${SOLSCAN_TX_URL}/${buyResult.signature}`,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error('[JellyChain] On-chain buyback failed:', errorMessage);
    return { success: false, error: errorMessage };
  }
}

export async function buyback(
  params: BuybackParams,
  options?: { rpcUrl?: string; pumpPortalApiKey?: string },
): Promise<BuybackResult> {
  if (options?.pumpPortalApiKey) {
    return buybackViaPortal(params, options.pumpPortalApiKey);
  }
  return buybackViaAnchor(params, options?.rpcUrl);
}
