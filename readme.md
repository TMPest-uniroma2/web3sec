# Blockchain Security Labs

This repository contains five hands-on labs designed for practitioners to understand and analyze the technical foundations and security aspects of blockchain-based systems, with a focus on both Ethereum and Hyperledger Fabric.

## Lab Overview

### 1. Foundational Understanding of PKI
This lab provides the building blocks of cryptographic identity and trust as applied to blockchain. Activities include:
- Generating key pairs and digital signatures
- Understanding x.509 certificates and certificate authorities
- Verifying signatures manually and programmatically
- Comparing Ethereum key handling (ECDSA) with Fabric's certificate-based identity (PKI)

### 2. Building Ethereum Infrastructure
This lab walks through setting up a realistic Ethereum-based environment with:
- Ganache as a local blockchain simulator
- Node.js CLI to create wallets, deploy and interact with smart contracts
- React frontend interacting with the blockchain via Web3.js
- Manual and programmatic signing, multisig wallets, reentrancy attack demonstration

### 3. Building Hyperledger Fabric Infrastructure
A permissioned blockchain setup using Hyperledger Fabric components:
- Two organizations with separate peers
- RAFT ordering service
- Chaincode deployment (both secure and intentionally flawed)
- Node.js client interacting with Fabric via the SDK
- Identity handling and chaincode access control using Fabric MSPs

### 4. Threat Modeling & Hardening
This lab introduces threat modeling specific to blockchain-based systems, covering:
- Security assumptions in smart contract platforms
- Common attack vectors: front-running, reentrancy, signature replay, phishing
- Web2 attack surfaces in dApps: XSS, clipboard hijack, DNS poisoning
- How to identify and apply hardening patterns at network, smart contract, and frontend layers

### 5. Distributed Attack Simulation and Detection
A simulation environment to explore the impact of distributed attacks:
- Sybil attack probability modeling
- Simulated reentrancy exploitation in Ethereum
- Peer isolation (eclipse-style) in Fabric using Docker overlay misconfigurations
- Collection and analysis of logs and metrics to detect anomalous behaviors
- Basics of monitoring for Ethereum and Fabric networks

## Requirements
- Docker + Docker Compose
- Node.js 18+
- GNU Make (for lab automation)
- Go 1.20+ (for Fabric chaincode)

# License
The project is released under MIT license.
