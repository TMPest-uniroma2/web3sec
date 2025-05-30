// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract FixedSigreplay {
    address public owner;
    mapping(uint256 => bool) public usedNonces;

    constructor(address _owner) payable {
        owner = _owner;
    }

    function withdraw(address to, uint256 amount, uint256 nonce, bytes memory signature) external {
        require(!usedNonces[nonce], "Nonce already used");

        bytes32 messageHash = keccak256(abi.encodePacked(address(this), to, amount, nonce));
        bytes32 ethSignedMessageHash = _toEthSignedMessageHash(messageHash);

        require(_recoverSigner(ethSignedMessageHash, signature) == owner, "Invalid signature");

        usedNonces[nonce] = true;

        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");
    }

    function deposit() external payable {}

    receive() external payable {}

    // ---- Minimal ECDSA ----

    function _toEthSignedMessageHash(bytes32 hash) internal pure returns (bytes32) {
        return keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", hash)
        );
    }

    function _recoverSigner(bytes32 ethSignedMessageHash, bytes memory signature) internal pure returns (address) {
        require(signature.length == 65, "ECDSA: invalid signature length");

        bytes32 r;
        bytes32 s;
        uint8 v;

        // ecrecover decompose
        assembly {
            r := mload(add(signature, 32))
            s := mload(add(signature, 64))
            v := byte(0, mload(add(signature, 96)))
        }

        return ecrecover(ethSignedMessageHash, v, r, s);
    }
}
