export * from './constants';
export * from './types';
export * from './wallet';
export * from './launch';
export * from './buyback';
export * from './lock';
export * from './claimFees';

import type { JellychainSDKConfig } from './types';
import { JellychainWallet } from './wallet';
import { launch } from './launch';
import { buyback } from './buyback';
import { lock } from './lock';
import { claimFees } from './claimFees';
import type {
  LaunchParams,
  LaunchResult,
  BuybackParams,
  BuybackResult,
  LockParams,
  LockResult,
  ClaimFeesParams,
  ClaimFeesResult,
} from './types';
import {
  SOLANA_MAINNET_RPC,
  DEFAULT_COMMITMENT,
  JELLYCHAIN_DOCS_URL,
  JELLYCHAIN_TERMINAL_URL,
} from './constants';

export class JellychainPumpFunSDK {
  private readonly config: Required<JellychainSDKConfig>;

  constructor(config: JellychainSDKConfig = {}) {
    this.config = {
      rpcUrl: config.rpcUrl ?? SOLANA_MAINNET_RPC,
      commitment: config.commitment ?? DEFAULT_COMMITMENT,
      pumpPortalApiKey: config.pumpPortalApiKey ?? '',
      priorityFeeSol: config.priorityFeeSol ?? 0.00005,
      slippageBps: config.slippageBps ?? 1500,
    };
  }

  get docsUrl(): string {
    return JELLYCHAIN_DOCS_URL;
  }

  get terminalUrl(): string {
    return JELLYCHAIN_TERMINAL_URL;
  }

  async launch(params: Omit<LaunchParams, 'priorityFeeSol' | 'slippageBps'> & Partial<Pick<LaunchParams, 'priorityFeeSol' | 'slippageBps'>>): Promise<LaunchResult> {
    return launch(
      {
        ...params,
        priorityFeeSol: params.priorityFeeSol ?? this.config.priorityFeeSol,
        slippageBps: params.slippageBps ?? this.config.slippageBps,
      },
      this.config.rpcUrl,
      this.config.pumpPortalApiKey || undefined,
    );
  }

  async buyback(params: Omit<BuybackParams, 'priorityFeeSol' | 'slippageBps'> & Partial<Pick<BuybackParams, 'priorityFeeSol' | 'slippageBps'>>): Promise<BuybackResult> {
    return buyback(
      {
        ...params,
        priorityFeeSol: params.priorityFeeSol ?? this.config.priorityFeeSol,
        slippageBps: params.slippageBps ?? this.config.slippageBps,
      },
      {
        rpcUrl: this.config.rpcUrl,
        pumpPortalApiKey: this.config.pumpPortalApiKey || undefined,
      },
    );
  }

  async lock(params: LockParams): Promise<LockResult> {
    return lock(params, this.config.rpcUrl);
  }

  async claimFees(params: ClaimFeesParams): Promise<ClaimFeesResult> {
    return claimFees(params, { rpcUrl: this.config.rpcUrl });
  }

  createWallet(): JellychainWallet {
    return JellychainWallet.generate();
  }

  walletFromBase58(privateKey: string): JellychainWallet {
    return JellychainWallet.fromBase58(privateKey);
  }
}

export default JellychainPumpFunSDK;
