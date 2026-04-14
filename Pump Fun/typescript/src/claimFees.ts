import {
  PublicKey,
  SystemProgram,
} from '@solana/web3.js';
import { Program, Idl } from '@coral-xyz/anchor';
import { getAssociatedTokenAddress, TOKEN_PROGRAM_ID } from '@solana/spl-token';
import {
  PUMPFUN_PROGRAM_ID,
  PUMPFUN_GLOBAL_ACCOUNT,
  PUMPFUN_EVENT_AUTHORITY,
  CREATOR_VAULT_SEED,
  BONDING_CURVE_SEED,
  SOLSCAN_TX_URL,
} from './constants';
import type { ClaimFeesParams, ClaimFeesResult } from './types';
import { JellychainWallet, createAnchorProvider } from './wallet';
import PUMPFUN_IDL from './idl/pumpfun.json';

export const PUMPFUN_PROGRAM_IDL = PUMPFUN_IDL;

export function deriveCreatorVaultPDA(
  mintAddress: PublicKey,
  creatorAddress: PublicKey,
): [PublicKey, number] {
  return PublicKey.findProgramAddressSync(
    [Buffer.from(CREATOR_VAULT_SEED), mintAddress.toBuffer(), creatorAddress.toBuffer()],
    PUMPFUN_PROGRAM_ID,
  );
}

export function deriveBondingCurvePDA(mintAddress: PublicKey): [PublicKey, number] {
  return PublicKey.findProgramAddressSync(
    [Buffer.from(BONDING_CURVE_SEED), mintAddress.toBuffer()],
    PUMPFUN_PROGRAM_ID,
  );
}

export async function getCreatorVaultBalance(
  mintAddress: string,
  creatorAddress: string,
  rpcUrl?: string,
): Promise<number> {
  const jellychainWallet = JellychainWallet.generate();
  const provider = createAnchorProvider(jellychainWallet, rpcUrl);

  const mint = new PublicKey(mintAddress);
  const creator = new PublicKey(creatorAddress);
  const [vaultPDA] = deriveCreatorVaultPDA(mint, creator);

  const balance = await provider.connection.getBalance(vaultPDA);
  return balance / 1e9;
}

export async function claimFeesViaAnchor(
  params: ClaimFeesParams,
  rpcUrl?: string,
): Promise<ClaimFeesResult> {
  const { wallet, mintAddress } = params;

  if (!mintAddress) {
    throw new Error('mintAddress is required for on-chain fee claim via Anchor');
  }

  try {
    const jellychainWallet = new JellychainWallet(wallet);
    const provider = createAnchorProvider(jellychainWallet, rpcUrl);

    const program = new Program(PUMPFUN_IDL as unknown as Idl, provider);

    const mint = new PublicKey(mintAddress);
    const [bondingCurve] = deriveBondingCurvePDA(mint);
    const [creatorVault] = deriveCreatorVaultPDA(mint, wallet.publicKey);

    const associatedBondingCurve = await getAssociatedTokenAddress(mint, bondingCurve, true);
    const associatedUser = await getAssociatedTokenAddress(mint, wallet.publicKey);

    console.log(`[JellyChain] Claiming fees for mint: ${mintAddress}`);
    console.log(`[JellyChain] Bonding curve:   ${bondingCurve.toBase58()}`);
    console.log(`[JellyChain] Creator vault:   ${creatorVault.toBase58()}`);

    const vaultBalance = await provider.connection.getBalance(creatorVault);
    if (vaultBalance === 0) {
      return {
        success: true,
        totalClaimedSol: 0,
        error: 'Creator vault is empty — no fees to claim',
      };
    }

    console.log(`[JellyChain] Creator vault balance: ${vaultBalance / 1e9} SOL`);

    const txSig = await (program.methods as any)
      .withdraw()
      .accounts({
        global: PUMPFUN_GLOBAL_ACCOUNT,
        mint,
        bondingCurve,
        associatedBondingCurve,
        creatorVault,
        creator: wallet.publicKey,
        associatedUser,
        systemProgram: SystemProgram.programId,
        tokenProgram: TOKEN_PROGRAM_ID,
        eventAuthority: PUMPFUN_EVENT_AUTHORITY,
        program: PUMPFUN_PROGRAM_ID,
      })
      .rpc({ commitment: 'confirmed' });

    console.log(`[JellyChain] Creator fees claimed: TX=${txSig}`);

    return {
      success: true,
      claimTxSignature: txSig,
      totalClaimedSol: vaultBalance / 1e9,
      solscanUrl: `${SOLSCAN_TX_URL}/${txSig}`,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error('[JellyChain] Anchor claim fees failed:', errorMessage);
    return { success: false, error: errorMessage };
  }
}

export async function claimFees(
  params: ClaimFeesParams,
  options?: { rpcUrl?: string; pumpPortalApiKey?: string },
): Promise<ClaimFeesResult> {
  return claimFeesViaAnchor(params, options?.rpcUrl);
}
