# Set container names
GANACHE_NAME=ganache
WALLETLAB_NAME=walletlab
REACT_NAME=react-app
RPC_SERVER := $(shell ip -4 addr show ens33 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
REACT_APP_RPC_SERVER=X

# Wrap walletlab command execution inside container
define walletlab
	sudo docker exec -it $(shell sudo docker ps | grep $(WALLETLAB_NAME) | head -n 1 | awk '{print $$1}') walletlab $(1)
endef

# Wrap walletlab direct command execution inside container
define wltest
	sudo docker exec -it $(shell sudo docker ps | grep $(WALLETLAB_NAME) | head -n 1 | awk '{print $$1}') npx mocha $(1)
endef

# Wrap walletlab direct command execution inside container
define wlmap
	sudo docker exec -it $(shell sudo docker ps | grep $(WALLETLAB_NAME) | head -n 1 | awk '{print $$1}') bash -c "cat ./config/contracts-map.json"
endef

# Wrap terminal access to Frontend
define debug_react
	sudo docker exec -it $(shell sudo docker ps | grep $(REACT_NAME) | head -n 1 | awk '{print $$1}') bash -c "echo '[*] Artifacts:' && ls src/artifacts; echo '[*] Contract mappings:' && ls src/config; echo '[*] Processes:' && ps aux"
endef

define react_install
	sudo docker exec -it $(shell sudo docker ps | grep $(REACT_NAME) | head -n 1 | awk '{print $$1}') bash -c "rm -rf node_modules && npm install"
endef

define react_start
	sudo docker exec -it $(shell sudo docker ps | grep $(REACT_NAME) | head -n 1 | awk '{print $$1}') bash -c "npm start"
endef

# Rebuild lab
build-containers:
	docker-compose build --no-cache
	exit

# Start Ganache and Walletlab
up:
	@sudo rm -rf ethereum-lab/ganache/*
	docker-compose up -d ganache walletlab
	exit

# Start Ganache and Walletlab
up-audit:
	docker-compose up -d mythril
	exit

# Compile contracts inside Walletlab container
compile:
	$(call walletlab,compile)
	exit

# Deploy multisig contract
deploy-all:
	$(call walletlab,deploy)
	$(call walletlab,deploy-reentrancy-vuln)
	$(call walletlab,deploy-sigreplay-vuln)
	exit

# Deploy multisig contract
deploy:
	$(call walletlab,deploy)
	exit

# Full setup: compile + deploy multisig + submit TX
fullsetup:
	$(call walletlab,fullsetup)
	exit

# Deploy vulnerable and attack contracts
deploy-vulns:
	$(call walletlab,deploy-reentrancy-vuln)
	$(call walletlab,deploy-sigreplay-vuln)
	exit

deploy-reentrancy-vuln:
	$(call walletlab,deploy-reentrancy-vuln)
	exit

deploy-sigreplay-vuln:
	$(call walletlab,deploy-sigreplay-vuln)
	exit

# Launch attack
attack-reentrancy:
	$(call walletlab,launch-reentrancy-attack$(if $(address), --attack $(address)))
	exit

attack-sigreplay:
	$(call walletlab,launch-sigreplay-attack$(if $(address), --attack $(address)))
	exit

# Recover wallet from mnemonic
recover:
	$(call walletlab,recover --mnemonic "$(mnemonic)" --showBalance)
	exit

contracts:
	$(call wlmap)
	exit

# Start React frontend
ui-up:
	REACT_APP_RPC_SERVER="http://$(RPC_SERVER):8545" docker-compose up -d react-app
	exit

# Stop React frontend
ui-down:
	docker-compose down react-app
	exit

# Run npm install on React frontend
ui-install-deps:
	$(call react_install)
	exit

# Start React frontend
ui-start:
	$(call react_start)
	exit

# Enter React frontend
ui-debug:
	$(call debug_react)
	exit

# Clean containers and volumes
clean:
	docker-compose down -v
	docker system prune -f --volumes
	exit

list:
	docker ps
	exit

logs:
	docker logs -f $(CONTAINER)
	exit

test:
	$(call wltest,test/test-multisig.js)
	exit

generate-certificate:
	@echo "[*] Generating certificates"
	@docker-compose up python-ca-manager
	exit

proxy-up:
	@echo "[*] Spinning up reverse proxy"
	@docker-compose up nginx-proxy -d
	exit

proxy-down:
	@echo "[*] Stopping reverse proxy"
	@docker-compose down nginx-proxy
	exit

audit:
	@echo "[*] Static audit: $(CONTRACT)"
	@docker exec mythril myth analyze contracts/$(CONTRACT)
	exit

audit-live:
	@echo "[+] Live audit on address: $(ADDRESS)"
	@docker exec mythril myth analyze -a $(ADDRESS) -rpc http://ganache:8545 --rpc --execution-timeout 120 --max-depth 50
	exit

audit-all:
	@echo "[*] Auditing all Solidity contracts in ./contracts/"
	@for f in $$(ls ./node-app/contracts/*.sol); do \
		echo "\n  [>] Analyzing $$f"; \
		docker exec mythril myth analyze $$f --solv 0.8.20 --output json | jq .; \
	done
	exit

# Stop all
down:
	docker-compose down -v
	exit

# Rebuild all
rebuild:
	docker-compose down -v
	docker system prune -f --volumes
	docker-compose build --no-cache
	make up
	exit
