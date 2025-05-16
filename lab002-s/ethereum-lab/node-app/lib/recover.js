import Web3 from 'web3';
import bip39 from 'bip39';
import { hdkey } from '@ethereumjs/wallet';

const recover = async (_, options) => {
    const { mnemonic, showBalance } = options;

    if (!mnemonic) {
        console.error("❌ Please provide --mnemonic");
        return;
    }

    const seed = await bip39.mnemonicToSeed(mnemonic);
    const hdWallet = hdkey.fromMasterSeed(seed);
    const key = hdWallet.derivePath("m/44'/60'/0'/0/0");
    const wallet = key.getWallet();

    const address = `0x${wallet.getAddress().toString('hex')}`;
    const privateKey = `0x${wallet.getPrivateKey().toString('hex')}`;

    console.log("✅ Wallet recovered:");
    console.log({ address, privateKey });

    if (showBalance) {
        const web3 = new Web3('http://ganache:8545');
        const balance = await web3.eth.getBalance(address);
        console.log("💰 Balance:", Web3.utils.fromWei(balance, 'ether'), "ETH");
    }
};

export default recover;
