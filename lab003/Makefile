# Makefile for Hyperledger Fabric Lab with Fablo

# Variables
BASE_DIR := ./fabric-lab/base
CONFIG_SRC := $(BASE_DIR)/config
CHAINCODE_SRC := $(BASE_DIR)/chaincode
FABLO_NETWORK_DIR := ./fablo-target
CHAINCODE_DIR := ./chaincode
BIN_DIR := ./bin
FABRIC_BIN_DIR := $(BIN_DIR)/fabric-binaries
CA_CLIENT_HOME := ./fabric-lab/fabric-ca-client
FABRIC_CA_URL := "https://github.com/hyperledger/fabric-ca/releases/download/v1.5.15/hyperledger-fabric-ca-linux-amd64-1.5.15.tar.gz"
CHAINCODE_DIRS := $(shell ls -1 $(CHAINCODE_SRC) 2>/dev/null)

# Default target
.PHONY: all
all: help

# Help text
.PHONY: help
help:
	@echo "Hyperledger Fabric Lab with Fablo - Make Targets:"
	@echo "  install-prereqs    - Install prerequisites (Docker, etc.)"
	@echo "  install-fablo      - Install Fablo tool"
	@echo "  install-fabric-bin - Install Fabric binaries (fabric-ca-client, etc.)"
	@echo "  setup              - Copy network config and chaincode files from base directory"
	@echo "  up                 - Start Fabric network"
	@echo "  down               - Stop Fabric network but keep artifacts"
	@echo "  clean              - Remove all artifacts and containers"
	@echo "  ca-setup           - Setup Fabric CA client environment"
	@echo "  register-user      - Register and enroll a new user with Fabric CA"
	@echo "  set-data           - Invoke SetData function on the chaincode"
	@echo "  get-data           - Query GetData function on the chaincode"
	@echo "  chaincode-install  - Rebuild and install chaincode"
	@echo "  explore-pki        - Explore the PKI infrastructure"
	@echo "  explore-network    - Show running containers and network details"

# Setup all chaincode directories
.PHONY: setup-chaincodes
setup-chaincodes:
	@echo "Discovered chaincode directories: $(CHAINCODE_DIRS)"
	@mkdir -p $(CHAINCODE_DIR)
	@for cc in $(CHAINCODE_DIRS); do \
		echo "Setting up chaincode: $$cc"; \
		mkdir -p $(CHAINCODE_DIR)/$$cc; \
		cp -rf $(CHAINCODE_SRC)/$$cc/* $(CHAINCODE_DIR)/$$cc/ 2>/dev/null || true; \
		cd $(CHAINCODE_DIR)/$$cc && \
			rm -f go.mod go.sum && \
			go mod init github.com/$$cc && \
			go get github.com/hyperledger/fabric-contract-api-go/contractapi@v1.2.1 && \
			go mod tidy && \
			go mod vendor; \
	done
	@echo "All chaincodes setup complete."

# Install prerequisites
.PHONY: install-prereqs
install-prereqs:
	@echo "Installing prerequisites..."
	sudo apt update
	sudo apt install -y git curl make jq

# Install Fablo
.PHONY: install-fablo
install-fablo:
	@echo "Installing Fablo..."
	sudo curl -Lf https://github.com/hyperledger-labs/fablo/releases/download/2.2.0/fablo.sh -o /usr/local/bin/fablo && sudo chmod +x /usr/local/bin/fablo
	fablo version

# Install Fabric CA client
.PHONY: install-fabric-bin
install-fabric-bin:
	@echo "Installing Fabric CA client v1.5.15..."
	@mkdir -p ./temp-ca-download
	@curl -sSL https://github.com/hyperledger/fabric-ca/releases/download/v1.5.15/hyperledger-fabric-ca-linux-amd64-1.5.15.tar.gz | tar xz -C ./temp-ca-download
	@sudo cp ./temp-ca-download/bin/fabric-ca-client /usr/local/bin/
	@sudo chmod +x /usr/local/bin/fabric-ca-client
	@rm -rf ./temp-ca-download
	@echo "Fabric CA client installed successfully. Version:"
	@fabric-ca-client version

# Setup network and chaincode files by copying from base directory
.PHONY: setup
setup:
	@echo "Setting up Fabric network configuration..."
	# Copy fablo-config.json from the base directory
	cp -f $(CONFIG_SRC)/fablo-config.json ./fablo-config.json

	# Setup all chaincodes
	$(MAKE) setup-chaincodes

	@echo "Setup complete. Configuration and all chaincodes copied and initialized."

# Show discovered chaincode directories
.PHONY: list-chaincodes
list-chaincodes:
	@echo "Discovered chaincode directories:"
	@for cc in $(CHAINCODE_DIRS); do echo " - $$cc"; done

# Start the Fabric network
.PHONY: up
up:
	@echo "Starting Fabric network..."
	fablo up

# Stop the Fabric network
.PHONY: down
down:
	@echo "Stopping Fabric network..."
	fablo down

# Clean up everything
.PHONY: clean
clean:
	@echo "Cleaning up Fabric network..."
	fablo clean

# Setup Fabric CA client environment
.PHONY: ca-setup
ca-setup:
	@echo "Setting up Fabric CA client environment..."
	mkdir -p $(CA_CLIENT_HOME)
	@echo "export FABRIC_CA_CLIENT_HOME=$(CURDIR)/$(CA_CLIENT_HOME)" >> ~/.bashrc
	@echo "export FABRIC_CA_CLIENT_TLS_CERTFILES=$(CURDIR)/$(FABLO_NETWORK_DIR)/fabric-config/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem" >> ~/.bashrc
	@echo "Please run 'source ~/.bashrc' after setup."

# Register and enroll a new user with Fabric CA
.PHONY: register-user
register-user:
	@echo "Registering and enrolling a new user with Fabric CA..."
	# Enroll admin first
	# Create a directory for Fabric CA client
	mkdir -p "$(FABRIC_CA_CLIENT_HOME)"
	mkdir -p "$(FABRIC_CA_CLIENT_HOME)/admin/msp"
	mkdir -p "$(FABRIC_CA_CLIENT_HOME)/user1/msp"
	fabric-ca-client enroll -u https://admin:adminpw@localhost:7054 --caname ca.org1.example.com --mspdir $(CA_CLIENT_HOME)/admin/msp
	# Register new user
	fabric-ca-client register --id.name user1 --id.secret user1pw --id.type client -u https://localhost:7054 --caname ca.org1.example.com --mspdir $(CA_CLIENT_HOME)/admin/msp
	# Enroll new user
	fabric-ca-client enroll -u https://user1:user1pw@localhost:7054 --caname ca.org1.example.com --mspdir $(CA_CLIENT_HOME)/user1/msp

# Invoke SetData function
.PHONY: set-data
set-data:
	@echo "Invoking SetData function on the chaincode..."
	fablo chaincode invoke "peer0.org1.example.com" "mychannel" "asset" '{"Args":["SetData", "asset3", "value-from-invoke"]}'

# Query GetData function
.PHONY: get-data
get-data:
	@echo "Querying GetData function on the chaincode..."
	fablo chaincode invoke "peer0.org1.example.com" "mychannel" "asset" '{"Args":["GetData", "asset3"]}'

# Install chaincode
.PHONY: chaincode-install
chaincode-install:
	echo "Installing chaincode $(CC) version 1.0..."
	fablo chaincode install "$(CC)" "1.0"

# Explore the PKI infrastructure
.PHONY: explore-pki
explore-pki:
	@echo "Exploring the PKI infrastructure..."
	@echo "Certificate Authority certificates:"
	ls -la $(FABLO_NETWORK_DIR)/fabric-config/crypto-config/peerOrganizations/org1.example.com/ca/
	@echo "\nMSP structure for peer0.org1:"
	ls -la $(FABLO_NETWORK_DIR)/fabric-config/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp/
	@echo "\nDisplaying a certificate example:"
	openssl x509 -in $(FABLO_NETWORK_DIR)/fabric-config/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp/signcerts/peer0.org1.example.com-cert.pem -text | head -30

# Explore the running network
.PHONY: explore-network
explore-network:
	@echo "Running Docker containers:"
	docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
	@echo "\nChannel information:"
	fablo channel getinfo mychannel

# Explore channels
.PHONY: list-channels
list-channels:
	@echo "List channels:"
	fablo channel list org1 peer0

.PHONY: list-channels
channel-info:
	@echo "Channel information:"
	fablo channel getinfo mychannel org1 peer0

