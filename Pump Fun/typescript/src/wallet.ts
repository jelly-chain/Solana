import {
  Connection,
  Keypair,
  Transaction,
  VersionedTransaction,
  PublicKey,
  Commitment,
} from '@solana/web3.js';
import { AnchorProvider } from '@coral-xyz/anchor';
import type { Wallet } from '@coral-xyz/anchor';
import bs58 from 'bs58';
import {
  SOLANA_MAINNET_RPC,
  DEFAULT_COMMITMENT,
} from './constants';

export class JellychainWallet implements Wallet {
  readonly payer: Keypair;

  constructor(keypair: Keypair) {
    this.payer = keypair;
  }

  get publicKey(): PublicKey {
    return this.payer.publicKey;
  }

  async signTransaction<T extends Transaction | VersionedTransaction>(tx: T): Promise<T> {
    if (tx instanceof Transaction) {
      tx.partialSign(this.payer);
    } else {
      tx.sign([this.payer]);
    }
    return tx;
  }

  async signAllTransactions<T extends Transaction | VersionedTransaction>(txs: T[]): Promise<T[]> {
    return txs.map((tx) => {
      if (tx instanceof Transaction) {
        tx.partialSign(this.payer);
      } else {
        tx.sign([this.payer]);
      }
      return tx;
    });
  }

  async signMessage(message: Uint8Array): Promise<Uint8Array> {
    throw new Error('signMessage is not supported in JellychainWallet');
  }

  static fromSecretKey(secretKey: Uint8Array): JellychainWallet {
    return new JellychainWallet(Keypair.fromSecretKey(secretKey));
  }

  static fromBase58(privateKeyBase58: string): JellychainWallet {
    const secretKey = bs58.decode(privateKeyBase58);
    return JellychainWallet.fromSecretKey(secretKey);
  }

  static generate(): JellychainWallet {
    return new JellychainWallet(Keypair.generate());
  }

  toBase58PrivateKey(): string {
    return bs58.encode(this.payer.secretKey);
  }
}

export function createConnection(
  rpcUrl: string = SOLANA_MAINNET_RPC,
  commitment: Commitment = DEFAULT_COMMITMENT,
): Connection {
  return new Connection(rpcUrl, {
    commitment,
    wsEndpoint: rpcUrl.replace('https://', 'wss://').replace('http://', 'ws://'),
  });
}

export function createAnchorProvider(
  wallet: JellychainWallet,
  rpcUrl: string = SOLANA_MAINNET_RPC,
  commitment: Commitment = DEFAULT_COMMITMENT,
): AnchorProvider {
  const connection = createConnection(rpcUrl, commitment);
  return new AnchorProvider(connection, wallet, { commitment });
}
