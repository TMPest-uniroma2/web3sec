import React, { useEffect, useState } from 'react';

import Web3 from "web3";
import contractsMap from "./config/contracts-map.json";
import multisigAbi from "./artifacts/SimpleMultiSigABI.json";
import vulnerableAbi from "./artifacts/Vulnerable2ReentrancyABI.json";
import attackAbi from "./artifacts/ReentrancyAttackABI.json";

function App() {
    const [web3, setWeb3] = useState(null);
    const [contracts, setContracts] = useState({});
    const [account, setAccount] = useState('');
    const [balance, setBalance] = useState('');
    const [destination, setDestination] = useState('');
    const [amount, setAmount] = useState('');
    const [txIndex, setTxIndex] = useState('');
    const [vulnBalance, setVulnBalance] = useState('');
    const [attackBalance, setAttackBalance] = useState('');

    useEffect(() => {
        async function load() {
            try {

                console.log(process.env.REACT_APP_RPC_SERVER);
                if (window.ethereum) {
                    window.web3 = new Web3(window.ethereum);
                    await window.ethereum.enable();
                } else if (window.web3) {
                    window.web3 = new Web3(new Web3.providers.HttpProvider(process.env.REACT_APP_RPC_SERVER));
                } else {
                    throw Error("This application requires an Ethereum browser to operate");
                }

                const web3 = window.web3;

                const chainId = await web3.eth.getChainId();
                const accounts = await web3.eth.getAccounts();
                setAccount(accounts[0]);

                const map = contractsMap[chainId];
                if (!map) throw new Error(`No contracts deployed on chain ID ${chainId}`);

                const contracts = {};
                if (map.SimpleMultiSig)
                    contracts.multisig = new web3.eth.Contract(multisigAbi, map.SimpleMultiSig);
                if (map.Vulnerable)
                    contracts.vulnerable = new web3.eth.Contract(vulnerableAbi, map.Vulnerable);
                if (map.ReentrancyAttack)
                    contracts.attacker = new web3.eth.Contract(attackAbi, map.ReentrancyAttack);

                setWeb3(web3);
                setContracts(contracts);

                const bal = await web3.eth.getBalance(accounts[0]);
                setBalance(web3.utils.fromWei(bal, 'ether'));

                if (map.Vulnerable) {
                    const vulnBal = await web3.eth.getBalance(contracts.vulnerable.options.address);
                    setVulnBalance(web3.utils.fromWei(vulnBal, 'ether'));
                }

                if (map.ReentrancyAttack){
                    const atkBal = await web3.eth.getBalance(contracts.attacker.options.address);
                    setAttackBalance(web3.utils.fromWei(atkBal, 'ether'));
                }
            } catch (err) {
                console.error("Web3 or contract setup failed:", err.message);
            }
        }

        load();
    }, []);

    const submitTransaction = async () => {
        try {
            console.log("Destination:", destination);
            console.log("Amount (ETH):", amount);

            if (!web3.utils.isAddress(destination)) throw new Error("Invalid address");
            if (!amount || isNaN(amount) || parseFloat(amount) <= 0) throw new Error("Invalid amount");

            const weiAmount = web3.utils.toWei(amount, 'ether');

            const receipt = await contracts.multisig.methods
                .submitTransaction(destination, weiAmount)
                .send({ from: account });

            console.log("TX Receipt:", receipt);
            alert('Transaction Submitted!');
        } catch (err) {
            console.error("Submit TX failed:", err.message);
            alert(`Transaction of ${amount} from ${account} to ${destination} failed: ${err.message}`);
        }
    };


    const confirmTransaction = async () => {
        await contracts.multisig.methods
            .confirmTransaction(txIndex)
            .send({ from: account });
        alert('Transaction Confirmed!');
    };

    const executeTransaction = async () => {
        await contracts.multisig.methods
            .executeTransaction(txIndex)
            .send({ from: account });
        alert('Transaction Executed!');
    };

    const depositToVulnerable = async () => {
        await contracts.vulnerable.methods.deposit().send({
            from: account,
            value: web3.utils.toWei('1', 'ether')
        });
        alert('Deposited to Vulnerable Contract!');
    };

    const launchAttack = async () => {
        await contracts.attacker.methods.attack().send({
            from: account,
            value: web3.utils.toWei('1', 'ether')
        });
        alert('Attack Launched!');
    };

    return (
        <div style={{ padding: '30px' }}>
            <h1>Blockchain Wallet Lab</h1>
            <h2>Account: {account}</h2>
            <h2>Balance: {balance} ETH</h2>

            <hr />
            <h3>SimpleMultiSig Actions</h3>
            <div>
                <input
                    type="text"
                    placeholder="Destination address"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Amount (ETH)"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                />
                <button onClick={submitTransaction}>Submit TX</button>
            </div>

            <div style={{ marginTop: '20px' }}>
                <input
                    type="text"
                    placeholder="Transaction Index"
                    value={txIndex}
                    onChange={(e) => setTxIndex(e.target.value)}
                />
                <button onClick={confirmTransaction}>Confirm TX</button>
                <button onClick={executeTransaction}>Execute TX</button>
            </div>

            <hr />
            <h3>Vulnerable Contract</h3>
            <p>Vulnerable Balance: {vulnBalance} ETH</p>
            <button onClick={depositToVulnerable}>Deposit 1 ETH</button>

            <hr />
            <h3>Attack Contract</h3>
            <p>Attack Contract Balance: {attackBalance} ETH</p>
            <button onClick={launchAttack}>Launch Reentrancy Attack</button>
        </div>
    );
}

export default App;
