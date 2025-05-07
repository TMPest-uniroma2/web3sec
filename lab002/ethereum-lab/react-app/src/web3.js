import Web3 from "web3";
import contractsMap from "./config/contracts-map.json";
import multisigAbi from "./artifacts/SimpleMultiSigABI.json";
import vulnerableAbi from "./artifacts/VulnerableABI.json";
import attackAbi from "./artifacts/ReentrancyAttackABI.json";

export const setupWeb3 = async () => {
    const web3 = new Web3(new Web3.providers.HttpProvider(process.env.REACT_APP_RPC_SERVER));
    const chainId = await web3.eth.getChainId();

    const map = contractsMap[chainId];
    if (!map) throw new Error(`No contracts deployed on chain ID ${chainId}`);

    const contracts = {
        multisig: new web3.eth.Contract(multisigAbi.abi, map.SimpleMultiSig),
        vulnerable: new web3.eth.Contract(vulnerableAbi.abi, map.Vulnerable),
        attacker: new web3.eth.Contract(attackAbi.abi, map.ReentrancyAttack),
    };

    return { web3, contracts };
};
