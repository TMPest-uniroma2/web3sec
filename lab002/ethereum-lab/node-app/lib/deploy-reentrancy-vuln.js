import Web3 from 'web3';
import fs from 'fs';
import { updateContractsMap } from './utils.js';

const deployReentrancyVuln = async () => {
    const web3 = new Web3('http://ganache:8545');
    const accounts = await web3.eth.getAccounts();
    const chainId = await web3.eth.getChainId();

    // Deploy vulnerable contract
    const vulnAbi = JSON.parse(fs.readFileSync('./artifacts/Vulnerable2ReentrancyABI.json'));
    const vulnBytecode = fs.readFileSync('./artifacts/Vulnerable2ReentrancyBytecode.txt', 'utf8');

    const vuln = new web3.eth.Contract(vulnAbi);
    const vulnInstance = await vuln.deploy({ data: vulnBytecode }).send({
        from: accounts[0],
        gas: 3000000
    });

    console.log("⚠️ Vulnerable contract deployed at:", vulnInstance.options.address);
    updateContractsMap("Vulnerable2Reentrancy", vulnInstance.options.address, chainId);

    await vulnInstance.methods.deposit().send({
        from: accounts[0],
        value: web3.utils.toWei('5', 'ether')
    });

    console.log("✅ Transaction sent!");

    // Deploy attack contract
    const atkAbi = JSON.parse(fs.readFileSync('./artifacts/ReentrancyAttackABI.json'));
    const atkBytecode = fs.readFileSync('./artifacts/ReentrancyAttackBytecode.txt', 'utf8');

    const attack = new web3.eth.Contract(atkAbi);
    const attackInstance = await attack.deploy({
        data: atkBytecode,
        arguments: [vulnInstance.options.address]
    }).send({
        from: accounts[1],
        gas: 6000000,
        value: '0'
    });

    console.log("✅ Reentrancy attack contract deployed at:", attackInstance.options.address);
    updateContractsMap("ReentrancyAttack", attackInstance.options.address, chainId);




};

export default deployReentrancyVuln;
