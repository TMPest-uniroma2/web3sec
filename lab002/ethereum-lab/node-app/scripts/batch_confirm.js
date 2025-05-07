const Web3 = require('web3');
const fs = require('fs');

async function batchConfirm() {
    const web3 = new Web3('http://127.0.0.1:8545');

    const abi = JSON.parse(fs.readFileSync('./artifacts/SimpleMultiSigABI.json'));
    const multisigAddress = '0xYourDeployedMultisigAddressHere';
    const multisig = new web3.eth.Contract(abi, multisigAddress);

    const accounts = await web3.eth.getAccounts();

    // Diamo per scontato che esistano 3 transazioni (ID: 0, 1, 2)
    for (let txIndex = 0; txIndex <= 2; txIndex++) {
        await multisig.methods.confirmTransaction(txIndex).send({ from: accounts[1], gas: 100000 });
        await multisig.methods.confirmTransaction(txIndex).send({ from: accounts[2], gas: 100000 });
        console.log(`Transaction ${txIndex} confirmed by accounts 1 and 2`);
    }
}

batchConfirm();
