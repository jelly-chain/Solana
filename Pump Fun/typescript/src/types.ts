import { PublicKey, Keypair, Commitment } from '@solana/web3.js';

export interface JellychainSDKConfig {
  rpcUrl?: string;
  commitment?: Commitment;
  pumpPortalApiKey?: string;
  priorityFeeSol?: number;
  slippageBps?: number;
}

export interface TokenMetadata {
  name: string;
  symbol: string;
  description: string;
  imageUrl: string;
  website?: string;
  twitter?: string;
  telegram?: string;
}

export interface LaunchParams {
  wallet: Keypair;
  metadata: TokenMetadata;
  devBuyAmountSol?: number;
  slippageBps?: number;
  priorityFeeSol?: number;
}

export interface LaunchResult {
  success: boolean;
  mintAddress?: string;
  mintKeypair?: Keypair;
  launchTxSignature?: string;
  devBuyTxSignature?: string;
  metadataUri?: string;
  solscanUrl?: string;
  pumpfunUrl?: string;
  error?: string;
}

export interface BuybackParams {
  wallet: Keypair;
  mintAddress: string;
  solAmount: number;
  slippageBps?: number;
  priorityFeeSol?: number;
  pool?: 'pump' | 'raydium';
}

export interface BuybackResult {
  success: boolean;
  txSignature?: string;
  solscanUrl?: string;
  tokensReceived?: number;
  error?: string;
}

export interface LockParams {
  wallet: Keypair;
  mintAddress: string;
  lockType?: 'burn' | 'renounce';
  amountTokens?: bigint;
  priorityFeeSol?: number;
}

export interface LockResult {
  success: boolean;
  txSignature?: string;
  solscanUrl?: string;
  lockedAmount?: string;
  lockType?: string;
  error?: string;
}

export interface ClaimFeesParams {
  wallet: Keypair;
  mintAddress?: string;
  priorityFeeSol?: number;
  recipientAddress?: string;
}

export interface ClaimFeesResult {
  success: boolean;
  claimTxSignature?: string;
  distributeTxSignature?: string;
  totalClaimedSol?: number;
  solscanUrl?: string;
  error?: string;
}

export interface PumpPortalWallet {
  walletPublicKey: string;
  privateKey: string;
  apiKey: string;
}

export interface PumpPortalIPFSResponse {
  metadataUri: string;
  metadata: {
    name: string;
    symbol: string;
    description: string;
    image: string;
    showName: boolean;
    createdOn: string;
    twitter?: string;
    telegram?: string;
    website?: string;
  };
}

export interface TokenInfo {
  mintAddress: string;
  name: string;
  symbol: string;
  description?: string;
  imageUrl?: string;
  metadataUri?: string;
  bondingCurveAddress?: string;
  creatorAddress?: string;
  pricePerToken?: number;
  marketCapSol?: number;
  virtualSolReserves?: bigint;
  virtualTokenReserves?: bigint;
  complete?: boolean;
}

export type Pool = 'pump' | 'raydium';
