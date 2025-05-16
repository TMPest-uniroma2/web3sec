const Web3 = require('web3');
const fs = require('fs');

async function batchSubmit() {
    const web3 = new Web3('http://127.0.0.1:8545');

    const abi = JSON.parse(fs.readFileSync('./artifacts/SimpleMultiSigABI.json'));
    const multisigAddress = '0xYourDeployedMultisigAddressHere';
    const multisig = new web3.eth.Contract(abi, multisigAddress);

    const accounts = await web3.eth.getAccounts();

    // Prepara un array di destinatari e amounts
    const targets = [
        { to: accounts[5], amount: '1' },
        { to: accounts[6], amount: '2' },
        { to: accounts[7], amount: '0.5' },
    ];

    for (let i = 0; i < targets.length; i++) {
        const tx = await multisig.methods.submitTransaction(
            targets[i].to,
            web3.utils.toWei(targets[i].amount, 'ether')
        ).send({ from: accounts[0], gas: 200000 });

        console.log(`Submitted transaction ${i} to ${targets[i].to}`);
    }
}

batchSubmit();
