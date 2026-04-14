import {
  PublicKey,
  Transaction,
} from '@solana/web3.js';
import {
  getAssociatedTokenAddress,
  createBurnInstruction,
  getAccount,
  TOKEN_PROGRAM_ID,
} from '@solana/spl-token';
import { Program, Idl } from '@coral-xyz/anchor';
import {
  BONDING_CURVE_SEED,
  PUMPFUN_PROGRAM_ID,
  SOLSCAN_TX_URL,
} from './constants';
import type { LockParams, LockResult } from './types';
import { JellychainWallet, createAnchorProvider } from './wallet';
import PUMPFUN_IDL from './idl/pumpfun.json';

export function deriveBondingCurvePDAForLock(mintAddress: PublicKey): [PublicKey, number] {
  return PublicKey.findProgramAddressSync(
    [Buffer.from(BONDING_CURVE_SEED), mintAddress.toBuffer()],
    PUMPFUN_PROGRAM_ID,
  );
}

export async function lock(
  params: LockParams,
  rpcUrl?: string,
): Promise<LockResult> {
  const { wallet, mintAddress } = params;

  try {
    const jellychainWallet = new JellychainWallet(wallet);
    const provider = createAnchorProvider(jellychainWallet, rpcUrl);

    const program = new Program(PUMPFUN_IDL as unknown as Idl, provider);

    const mint = new PublicKey(mintAddress);
    const [bondingCurve] = deriveBondingCurvePDAForLock(mint);

    let bcState: { virtualTokenReserves: bigint; complete: boolean } | null = null;
    try {
      bcState = await (program.account as any).bondingCurveAccount.fetch(bondingCurve);
    } catch {
      return {
        success: false,
        error: `No bonding curve account found for mint ${mintAddress} — not a valid Pump.fun token`,
      };
    }

    if (bcState.complete) {
      return {
        success: false,
        error: 'Bonding curve is complete (token graduated) — lock dev tokens before graduation',
      };
    }

    console.log(`[JellyChain] Bonding curve: ${bondingCurve.toBase58()} (reserves: ${bcState.virtualTokenReserves.toString()})`);

    const walletAta = await getAssociatedTokenAddress(mint, wallet.publicKey);
    const walletAtaInfo = await provider.connection.getAccountInfo(walletAta);

    if (!walletAtaInfo) {
      return { success: false, error: 'No token account found for this wallet/mint combination' };
    }

    const tokenAccount = await getAccount(provider.connection, walletAta);
    const totalAmount = tokenAccount.amount;

    if (totalAmount === BigInt(0)) {
      return { success: false, error: 'No tokens to lock — wallet balance is 0' };
    }

    const lockAmount = params.amountTokens ?? totalAmount;

    if (lockAmount > totalAmount) {
      return {
        success: false,
        error: `Requested lock amount ${lockAmount} exceeds balance ${totalAmount}`,
      };
    }

    console.log(
      `[JellyChain] Locking ${lockAmount} tokens (burn) for mint: ${mintAddress}`,
    );

    const burnIx = createBurnInstruction(
      walletAta,
      mint,
      wallet.publicKey,
      lockAmount,
      [],
      TOKEN_PROGRAM_ID,
    );

    const transaction = new Transaction().add(burnIx);
    const { blockhash } = await provider.connection.getLatestBlockhash();
    transaction.recentBlockhash = blockhash;
    transaction.feePayer = wallet.publicKey;

    const signature = await provider.sendAndConfirm(transaction, [wallet], {
      commitment: 'confirmed',
    });

    console.log(`[JellyChain] ${lockAmount} tokens burned (locked), TX=${signature}`);

    return {
      success: true,
      txSignature: signature,
      solscanUrl: `${SOLSCAN_TX_URL}/${signature}`,
      lockedAmount: lockAmount.toString(),
      lockType: 'burn',
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error('[JellyChain] Lock failed:', errorMessage);
    return { success: false, error: errorMessage };
  }
}
