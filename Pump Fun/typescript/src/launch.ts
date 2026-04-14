import { Keypair } from '@solana/web3.js';
import bs58 from 'bs58';
import {
  PUMPPORTAL_IPFS_URL,
  PUMPPORTAL_TRADE_URL,
  PUMPPORTAL_CREATE_WALLET_URL,
  SOLSCAN_TX_URL,
  PUMPFUN_TOKEN_URL,
  DEFAULT_SLIPPAGE_BPS,
  DEFAULT_PRIORITY_FEE_SOL,
} from './constants';
import type {
  LaunchParams,
  LaunchResult,
  TokenMetadata,
  PumpPortalWallet,
  PumpPortalIPFSResponse,
} from './types';

async function uploadMetadataToPumpPortal(metadata: TokenMetadata): Promise<string> {
  const formData = new FormData();
  formData.append('name', metadata.name);
  formData.append('symbol', metadata.symbol);
  formData.append('description', metadata.description);
  formData.append('showName', 'true');

  if (metadata.twitter) formData.append('twitter', metadata.twitter);
  if (metadata.telegram) formData.append('telegram', metadata.telegram);
  if (metadata.website) formData.append('website', metadata.website);

  let imageBlob: Blob;
  if (metadata.imageUrl.startsWith('data:')) {
    const [header, base64Data] = metadata.imageUrl.split(',');
    const mimeType = header.split(':')[1].split(';')[0];
    const binaryStr = atob(base64Data);
    const bytes = new Uint8Array(binaryStr.length);
    for (let i = 0; i < binaryStr.length; i++) bytes[i] = binaryStr.charCodeAt(i);
    imageBlob = new Blob([bytes], { type: mimeType });
  } else {
    const imgResponse = await fetch(metadata.imageUrl);
    if (!imgResponse.ok) {
      throw new Error(`Failed to fetch image from ${metadata.imageUrl}: ${imgResponse.statusText}`);
    }
    imageBlob = await imgResponse.blob();
  }

  formData.append('file', imageBlob, 'token-image.png');

  const response = await fetch(PUMPPORTAL_IPFS_URL, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`PumpPortal IPFS upload failed (${response.status}): ${text}`);
  }

  const data = (await response.json()) as PumpPortalIPFSResponse;
  if (!data.metadataUri) {
    throw new Error('PumpPortal IPFS upload returned no metadataUri');
  }

  return data.metadataUri;
}

export async function createPumpPortalWallet(): Promise<PumpPortalWallet> {
  const response = await fetch(PUMPPORTAL_CREATE_WALLET_URL, { method: 'GET' });
  if (!response.ok) {
    throw new Error(`PumpPortal create-wallet failed (${response.status}): ${await response.text()}`);
  }
  const raw = (await response.json()) as Record<string, string>;
  if (!raw.walletPublicKey || !raw.privateKey || !raw.apiKey) {
    throw new Error('PumpPortal create-wallet returned incomplete wallet data');
  }
  return {
    walletPublicKey: raw.walletPublicKey,
    privateKey: raw.privateKey,
    apiKey: raw.apiKey,
  };
}

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

export async function launch(
  params: LaunchParams,
  rpcUrl?: string,
  pumpPortalApiKey?: string,
): Promise<LaunchResult> {
  const { wallet, metadata, devBuyAmountSol = 0 } = params;
  const slippageBps = params.slippageBps ?? DEFAULT_SLIPPAGE_BPS;
  const priorityFee = params.priorityFeeSol ?? DEFAULT_PRIORITY_FEE_SOL;

  try {
    let apiKey = pumpPortalApiKey;
    let lightningWallet: PumpPortalWallet | null = null;

    if (!apiKey) {
      console.log('[JellyChain] Creating PumpPortal lightning wallet...');
      lightningWallet = await createPumpPortalWallet();
      apiKey = lightningWallet.apiKey;
    }

    console.log('[JellyChain] Uploading token metadata to IPFS via PumpPortal...');
    const metadataUri = await uploadMetadataToPumpPortal(metadata);
    console.log(`[JellyChain] Metadata URI: ${metadataUri}`);

    const mintKeypair = Keypair.generate();
    const mintAddress = mintKeypair.publicKey.toBase58();
    const mintPrivateKeyB58 = bs58.encode(mintKeypair.secretKey);

    const buyAmount = devBuyAmountSol > 0 ? devBuyAmountSol : 0.0001;

    console.log(`[JellyChain] Creating token ${metadata.symbol} (${mintAddress})...`);

    const createPayload = {
      action: 'create',
      tokenMetadata: {
        name: metadata.name,
        symbol: metadata.symbol,
        uri: metadataUri,
      },
      mint: mintPrivateKeyB58,
      denominatedInSol: 'true',
      amount: buyAmount,
      slippage: Math.floor(slippageBps / 100),
      priorityFee,
      pool: 'pump',
    };

    const createResult = await callPumpPortal(apiKey, createPayload);
    const launchTxSignature = createResult.signature;

    console.log(`[JellyChain] Token launched! Mint: ${mintAddress}, TX: ${launchTxSignature}`);

    return {
      success: true,
      mintAddress,
      mintKeypair,
      launchTxSignature,
      devBuyTxSignature: devBuyAmountSol > 0 ? launchTxSignature : undefined,
      metadataUri,
      solscanUrl: `${SOLSCAN_TX_URL}/${launchTxSignature}`,
      pumpfunUrl: `${PUMPFUN_TOKEN_URL}/${mintAddress}`,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error('[JellyChain] Launch failed:', errorMessage);
    return { success: false, error: errorMessage };
  }
}
