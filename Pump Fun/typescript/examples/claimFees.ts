import { JellychainPumpFunSDK } from '../src';

async function main() {
  const sdk = new JellychainPumpFunSDK({
    rpcUrl: process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
    pumpPortalApiKey: process.env.PUMP_PORTAL_API_KEY!,
  });

  const wallet = sdk.walletFromBase58(process.env.PRIVATE_KEY_BASE58!);

  console.log('[JellyChain] Claiming creator fees...');
  console.log('Wallet:', wallet.publicKey.toBase58());

  const result = await sdk.claimFees({
    wallet: wallet.payer,
    recipientAddress: process.env.RECIPIENT_ADDRESS || wallet.publicKey.toBase58(),
  });

  if (result.success) {
    console.log('Fees claimed!');
    console.log('Total claimed:', result.totalClaimedSol, 'SOL');
    console.log('Claim TX:', result.claimTxSignature);
    if (result.distributeTxSignature) {
      console.log('Distribute TX:', result.distributeTxSignature);
    }
    console.log('Solscan:', result.solscanUrl);
  } else {
    console.error('Claim failed:', result.error);
  }
}

main().catch(console.error);
