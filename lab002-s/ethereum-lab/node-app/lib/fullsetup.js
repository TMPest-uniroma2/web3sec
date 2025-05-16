import Web3 from 'web3';
import bip39 from 'bip39';
import { hdkey } from '@ethereumjs/wallet';
import fs from 'fs';

import { updateContractsMap } from './utils.js';

const fullsetup = async () => {
    const web3 = new Web3('http://ganache:8545');
    const ganacheAccounts = await web3.eth.getAccounts();
    const chainId = await web3.eth.getChainId();

    // Generate HD wallet
    const mnemonic = bip39.generateMnemonic();
    const seed = await bip39.mnemonicToSeed(mnemonic);
    const hdWallet = hdkey.fromMasterSeed(seed);
    const key = hdWallet.derivePath("m/44'/60'/0'/0/0");
    const wallet = key.getWallet();
    const address = `0x${wallet.getAddress().toString('hex')}`;
    const privateKey = wallet.getPrivateKey().toString('hex');

    console.log("🪙 Custom Wallet Generated:");
    console.log({ mnemonic, address, privateKey });

    // Fund wallet from Ganache[0]
    await web3.eth.sendTransaction({
        from: ganacheAccounts[0],
        to: address,
        value: web3.utils.toWei('10', 'ether'),
    });

    // Load contract
    const abi = JSON.parse(fs.readFileSync('./artifacts/SimpleMultiSigABI.json'));
    const bytecode = fs.readFileSync('./artifacts/SimpleMultiSigBytecode.txt', 'utf8');

    const acct = web3.eth.accounts.privateKeyToAccount('0x' + privateKey);
    web3.eth.accounts.wallet.add(acct);

    const multisig = new web3.eth.Contract(abi);
    const owners = [address, ganacheAccounts[1], ganacheAccounts[2]];

    // Deploy
    const deployed = await multisig.deploy({
        data: bytecode,
        arguments: [owners, 2]
    }).send({
        from: address,
        gas: 3000000,
    });

    console.log("✅ Multisig deployed at:", deployed.options.address);
    updateContractsMap("SimpleMultiSig", deployed.options.address, chainId);

    // Submit test transaction
    await deployed.methods.submitTransaction(ganacheAccounts[3], web3.utils.toWei('1', 'ether'))
        .send({ from: address, gas: 150000 });

    console.log("🚀 Submitted TX from multisig to:", ganacheAccounts[3]);
};

export default fullsetup;
