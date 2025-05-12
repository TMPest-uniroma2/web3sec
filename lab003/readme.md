# Hyperledger Fabric Lab: Permissioned Blockchain Exploration

## Overview

This lab provides a hands-on approach to understanding and working with Hyperledger Fabric, an enterprise-grade permissioned blockchain platform. The lab covers basic setup, configuration, and interaction with a Hyperledger Fabric network using Fablo, a simplified orchestration tool designed for development and testing.

## Learning Objectives

- Understand the key components of a permissioned blockchain network
- Configure and deploy a Hyperledger Fabric network with multiple organizations
- Explore the Public Key Infrastructure (PKI) and certificate management
- Develop, deploy, and interact with smart contracts (chaincode)
- Understand the consortium governance model in Fabric
- Create a simple client application for interacting with the blockchain

## Lab Architecture

The lab creates a Fabric network with the following components:

- **Organizations**: Two organizations (Org1 and Org2) participating in the network
- **Peers**: Each organization has two peer nodes for endorsing transactions
- **Ordering Service**: A solo orderer for transaction ordering and block creation
- **Certificate Authorities**: Each organization has its own CA for identity management
- **Channel**: A private communication channel ("mychannel") between organizations
- **Chaincode**: A smart contract implementing SetData and GetData functions

### Vulnerable chaincode - Race Conditions & Authorization Flaws

These codes demonstrates common logic-level vulnerabilities in permissioned blockchain smart contracts. Two insecure patterns are explored:

1. **Data Race / Double-Spend Condition**: A chaincode that fails to account for MVCC concurrency, allowing inconsistent balance updates.
2. **Weak Authorization**: A chaincode that lacks identity validation, permitting unauthorized writes.

## Prerequisites

- Docker and Docker Compose
- Go Programming Language (1.16 or higher)
- Git
- Fablo (Hyperledger Fabric orchestration tool)
- Python 3.8+ (for web interface)

## Lab Components

### 1. Network Setup Using Fablo

Fablo simplifies the deployment of Fabric networks for development purposes. The configuration file (`fablo-config.json`) defines the network topology, organizations, and components.

### 2. Chaincode Development

The lab includes sample chaincode written in Go that implements key-value storage functionality:

- `SetData`: Stores a key-value pair on the ledger
- `GetData`: Retrieves a value associated with a key from the ledger

### 3. PKI and Identity Management

Hyperledger Fabric uses a Public Key Infrastructure (PKI) for identity verification:

- Each organization has its own Certificate Authority (CA)
- The CA issues certificates to administrators, peers, and users
- These certificates are used to sign and validate transactions

### 4. Governance Model

The lab demonstrates Fabric's consortium governance model:

- Multiple organizations form a consortium
- Endorsement policies define which organizations must validate transactions
- The channel configuration defines the rules for participating in the network

### 5. Client Application

A Python web interface demonstrates how applications can interact with the blockchain:

- Connect to the Fabric network
- Submit transactions to invoke chaincode
- Query the ledger to retrieve data

## Lab Structure

```
Makefile                       # Automation scripts
fabric-lab/
├── base/                      # Base configuration files
│   ├── config/                # Network configuration
│   └── chaincode/             # Chaincode source code
├── frontend/                  # Python web interface
└── sast/                      # SAST tools
```

## Key Commands

The lab includes a Makefile to simplify common operations:

- `make setup`: Copy configuration and chaincode from base directory
- `make up`: Start the Fabric network
- `make down`: Stop the Fabric network
- `make chaincode-install CC=asset`: Install the specified chaincode
- `make set-data`: Invoke the SetData function
- `make get-data`: Query the GetData function
- `make explore-pki`: Explore the PKI infrastructure
- `make clean`: Remove all artifacts and containers

## Understanding Permissioned Blockchains

Unlike public blockchains like Bitcoin or Ethereum, Hyperledger Fabric is a permissioned blockchain where:

1. **Identity is Known**: All participants have known identities managed by PKI
2. **Privacy is Prioritized**: Data is shared only with authorized participants
3. **Performance is Scalable**: Consensus mechanisms are optimized for enterprise use
4. **Governance is Consortium-Based**: Multiple organizations collaboratively manage the network

## Conclusion

By completing this lab, (hopefully) students will have a foundation for 
developing permissioned blockchain solutions using Hyperledger Fabric.