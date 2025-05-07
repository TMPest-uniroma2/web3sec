import Web3 from 'web3';

const fund = async (address, options) => {
    const amount = options.amount || '5';

    const web3 = new Web3('http://ganache:8545');
    const accounts = await web3.eth.getAccounts();

    await web3.eth.sendTransaction({
        from: accounts[0],
        to: address,
        value: web3.utils.toWei(amount, 'ether'),
    });

    console.log(`✅ Sent ${amount} ETH to ${address}`);
};

export default fund;
