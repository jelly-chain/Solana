import { JellychainPumpFunSDK } from '../src';

async function main() {
  const sdk = new JellychainPumpFunSDK({
    rpcUrl: process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
  });

  const wallet = sdk.walletFromBase58(process.env.PRIVATE_KEY_BASE58!);
  const mintAddress = process.env.MINT_ADDRESS!;

  console.log('[JellyChain] Locking dev tokens...');
  console.log('Wallet:', wallet.publicKey.toBase58());
  console.log('Mint:', mintAddress);

  const result = await sdk.lock({
    wallet: wallet.payer,
    mintAddress,
    lockType: 'burn',
  });

  if (result.success) {
    console.log('Tokens locked!');
    console.log('Locked amount:', result.lockedAmount);
    console.log('Lock type:', result.lockType);
    console.log('TX:', result.txSignature);
    console.log('Solscan:', result.solscanUrl);
  } else {
    console.error('Lock failed:', result.error);
  }
}

main().catch(console.error);
