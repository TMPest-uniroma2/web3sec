// contracts/SimpleMultiSig.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleMultiSig {
    address[] public owners;
    uint public required;
    mapping (uint => Transaction) public transactions;
    uint public txCount;

    struct Transaction {
        address destination;
        uint value;
        bool executed;
        uint confirmations;
    }

    mapping (uint => mapping (address => bool)) public confirmations;

    constructor(address[] memory _owners, uint _required) {
        owners = _owners;
        required = _required;
    }

    function submitTransaction(address destination, uint value) public returns (uint) {
        uint txIndex = txCount;
        transactions[txIndex] = Transaction(destination, value, false, 0);
        txCount++;
        confirmTransaction(txIndex);
        return txIndex;
    }

    function confirmTransaction(uint txIndex) public {
        require(!confirmations[txIndex][msg.sender], "Already confirmed");
        confirmations[txIndex][msg.sender] = true;
        transactions[txIndex].confirmations++;
        if (transactions[txIndex].confirmations >= required) {
            executeTransaction(txIndex);
        }
    }

    function executeTransaction(uint txIndex) internal {
        Transaction storage txn = transactions[txIndex];
        require(!txn.executed, "Already executed");
        txn.executed = true;
        (bool success, ) = payable(txn.destination).call{value: txn.value}("");
        require(success, "Transfer failed");
    }

    receive() external payable {}
}
