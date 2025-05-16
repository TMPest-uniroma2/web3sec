import web3 from "./web3";
import abi from "./abi.json";

const address = "0xYourMultisigContractAddressHere"; // <-- sostituire!

const multisig = new web3.eth.Contract(abi, address);

export default multisig;
