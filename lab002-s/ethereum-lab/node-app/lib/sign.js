import Web3 from 'web3';

const sign = async (_, options) => {
    const { to, value, privkey } = options;

    if (!to || !value || !privkey) {
        console.error("❌ Missing --to, --value or --privkey");
        return;
    }

    const web3 = new Web3('http://ganache:8545');
    const account = web3.eth.accounts.privateKeyToAccount(privkey);
    const nonce = await web3.eth.getTransactionCount(account.address);

    const tx = {
        to,
        value: web3.utils.toWei(value, 'ether'),
        gas: 21000,
        nonce,
        chainId: 1337
    };

    const signed = await account.signTransaction(tx);
    const receipt = await web3.eth.sendSignedTransaction(signed.rawTransaction);

    console.log(`✅ TX sent: ${receipt.transactionHash}`);
};

export default sign;
