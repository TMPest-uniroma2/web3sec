## Lab 2: Blockchain Security Engineering - Practical Smart Contract Exploitation

### Overview

This lab provides a practical environment for analyzing and exploiting vulnerabilities in Ethereum smart contracts. It uses a Docker-based setup to simulate a local blockchain (Ganache), a CLI tool (`walletlab`) for contract management and attack orchestration, and a React frontend for interacting with smart contracts.

The lab is structured around deployment, interaction, and exploitation of smart contracts, with an additional focus on reverse engineering EVM bytecode.

---

### Lab Objectives

1. **Deploy and interact with a secure multisig wallet**
2. **Deploy and exploit two vulnerable contracts:**

    * A contract vulnerable to **reentrancy**
    * A contract vulnerable to **signature replay**
3. **Perform static analysis using Mythril**
4. **Reverse engineer contract bytecode manually**
5. **Interact with contracts through both frontend and CLI**

---

### Prerequisites

* Docker and Docker Compose installed
* Basic familiarity with smart contracts and JavaScript
* Optional: familiarity with Metamask and Etherscan

---

### Setup Instructions

Build and start all containers:

```bash
make rebuild
```

Compile contracts:

```bash
make compile
```

Deploy all contracts:

```bash
make deploy-all
```

Start the React frontend:

```bash
make ui-up
```

---

### Available Make Targets

| Target              | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `compile`           | Compile all contracts in the `contracts/` directory   |
| `deploy-all`        | Deploy multisig, reentrancy vuln, and sigreplay vuln  |
| `fullsetup`         | Compile and deploy multisig + submit initial TX       |
| `attack-reentrancy` | Launch reentrancy exploit from attack contract        |
| `attack-sigreplay`  | Launch signature replay exploit                       |
| `recover`           | Recover HD wallet from mnemonic and show balance      |
| `audit`             | Run Mythril static analysis on a specific contract    |
| `audit-all`         | Run Mythril on all Solidity contracts                 |
| `test`              | Run Mocha tests inside `walletlab`                    |
| `ui-up` / `ui-down` | Start or stop the React frontend                      |
| `contracts`         | Show deployed contract addresses (from contracts-map) |

---

### Bytecode Reverse Engineering

As part of this lab, you'll manually analyze contract bytecode to understand:

* How to identify public function selectors (`0x`-prefixed 4-byte values)
* How to match function selectors with ABI definitions
* How to observe and compare runtime behavior vs. decompiled intent

This includes:

* Inspecting deployed bytecode in `./artifacts/`
* Matching opcode sequences to Solidity constructs (e.g. `CALL`, `JUMPI`)
* Using Etherscan bytecode viewers (if connected to live chains)

---

### Notes

* Contract addresses are written to `config/contracts-map.json`
* React frontend loads ABI and addresses dynamically from `src/config/`
* For direct CLI usage inside the container: `docker exec -it walletlab bash`