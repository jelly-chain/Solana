import { JellychainPumpFunSDK, JellychainWallet } from '../src';

async function main() {
  const sdk = new JellychainPumpFunSDK({
    rpcUrl: process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
    pumpPortalApiKey: process.env.PUMP_PORTAL_API_KEY,
    slippageBps: 2000,
  });

  const wallet = sdk.walletFromBase58(process.env.PRIVATE_KEY_BASE58!);
  const mintAddress = process.env.MINT_ADDRESS!;

  console.log('[JellyChain] Executing buyback...');
  console.log('Wallet:', wallet.publicKey.toBase58());
  console.log('Mint:', mintAddress);

  const result = await sdk.buyback({
    wallet: wallet.payer,
    mintAddress,
    solAmount: 0.5,
    pool: 'pump',
  });

  if (result.success) {
    console.log('Buyback successful!');
    console.log('TX:', result.txSignature);
    console.log('Solscan:', result.solscanUrl);
  } else {
    console.error('Buyback failed:', result.error);
  }
}

main().catch(console.error);
