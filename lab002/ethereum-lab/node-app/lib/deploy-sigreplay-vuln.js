import Web3 from 'web3';
import fs from 'fs';
import { updateContractsMap } from './utils.js';

const deploySigreplayVuln = async () => {
    const web3 = new Web3('http://ganache:8545');
    const accounts = await web3.eth.getAccounts();
    const chainId = await web3.eth.getChainId();

    // Deploy vulnerable contract
    const vulnAbi = JSON.parse(fs.readFileSync('./artifacts/Vulnerable2SigreplayABI.json'));
    const vulnBytecode = fs.readFileSync('./artifacts/Vulnerable2SigreplayBytecode.txt', 'utf8');

    const vuln = new web3.eth.Contract(vulnAbi);
    const vulnInstance = await vuln
        .deploy({
            data: vulnBytecode,
            arguments: [accounts[0]]
        })
        .send({
            from: accounts[0],
            gas: 6000000,
            value: 0 // esplicito per compatibilità
        });

    console.log("⚠️ Vulnerable contract deployed at:", vulnInstance.options.address);
    updateContractsMap("Vulnerable2Sigreplay", vulnInstance.options.address, chainId);

    await vulnInstance.methods.deposit().send({
        from: accounts[0],
        value: web3.utils.toWei('5', 'ether')
    });
};

export default deploySigreplayVuln;
