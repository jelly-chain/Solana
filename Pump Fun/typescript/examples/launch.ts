import { JellychainPumpFunSDK, JellychainWallet } from '../src';

async function main() {
  const sdk = new JellychainPumpFunSDK({
    rpcUrl: process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
    pumpPortalApiKey: process.env.PUMP_PORTAL_API_KEY,
    slippageBps: 1500,
    priorityFeeSol: 0.00005,
  });

  const wallet = process.env.PRIVATE_KEY_BASE58
    ? sdk.walletFromBase58(process.env.PRIVATE_KEY_BASE58)
    : sdk.createWallet();

  console.log('Wallet:', wallet.publicKey.toBase58());
  console.log('Docs:', sdk.docsUrl);

  const result = await sdk.launch({
    wallet: wallet.payer,
    metadata: {
      name: 'Jelly Token',
      symbol: 'JELLY',
      description: 'The official JellyChain memecoin — powered by https://jellychain.fun',
      imageUrl: 'https://picsum.photos/500/500',
      twitter: 'https://twitter.com/jellychain',
      telegram: 'https://t.me/jellychain',
      website: 'https://jellychain.fun',
    },
    devBuyAmountSol: 0.1,
  });

  if (result.success) {
    console.log('Token launched!');
    console.log('Mint address:', result.mintAddress);
    console.log('TX:', result.launchTxSignature);
    console.log('Solscan:', result.solscanUrl);
    console.log('Pump.fun:', result.pumpfunUrl);
  } else {
    console.error('Launch failed:', result.error);
  }
}

main().catch(console.error);
