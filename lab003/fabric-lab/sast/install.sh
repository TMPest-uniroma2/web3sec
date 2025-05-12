#!/usr/bin/env bash

if [ ! -f "/usr/local/bin/ccanalyzer" ]; then
  git clone https://github.com/hyperledger-labs/chaincode-analyzer.git
  pushd chaincode-analyzer || die
  go mod init github.com/hyperledger-labs/chaincode-analyzer
  go mod tidy
  go mod vendor
  go build ccanalyzer.go
  sudo ln -s "${PWD}/ccanalyzer" "/usr/local/bin/ccanalyzer"
  popd || die
fi

if [ ! -f "/usr/local/bin/revive-cc" ]; then
  git clone https://github.com/sivachokkapu/revive-cc.git
  pushd revive-cc || die
  go mod init github.com/hyperledger-labs/chaincode-analyzer
  go mod tidy
  go mod vendor
  go build
  sudo ln -s "${PWD}/revive" "/usr/local/bin/revive"
fi