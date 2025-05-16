import Web3 from 'web3';
import fs from 'fs';
import { updateContractsMap } from './utils.js';

const deploy = async () => {
    const web3 = new Web3('http://ganache:8545');
    const accounts = await web3.eth.getAccounts();
    const chainId = await web3.eth.getChainId();

    const abi = JSON.parse(fs.readFileSync('./artifacts/SimpleMultiSigABI.json'));
    const bytecode = fs.readFileSync('./artifacts/SimpleMultiSigBytecode.txt', 'utf8');

    const multisig = new web3.eth.Contract(abi);
    const deployed = await multisig.deploy({
        data: bytecode,
        arguments: [accounts.slice(0, 3), 2]
    }).send({
        from: accounts[0],
        gas: 3000000
    });

    console.log("✅ Multisig deployed at:", deployed.options.address);

    updateContractsMap("SimpleMultiSig", deployed.options.address, chainId);
};

export default deploy;
