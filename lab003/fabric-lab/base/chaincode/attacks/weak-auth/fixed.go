package main

import (
    "fmt"
    "strings"

    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SecureContract defines the contract structure
type SecureContract struct {
    contractapi.Contract
}

// OnlyOrg1Admin can write data (simplified identity check)
func (s *SecureContract) WriteData(ctx contractapi.TransactionContextInterface, key string, value string) error {
    clientID, err := ctx.GetClientIdentity().GetID()
    if err != nil {
        return fmt.Errorf("failed to get client identity: %v", err)
    }

    // Only Org1 admins allowed (this is a simplified check! Not in prod guys!)
    if !strings.Contains(clientID, "Org1MSP") {
        return fmt.Errorf("unauthorized: only Org1 members can write data")
    }

    if key == "" || value == "" {
        return fmt.Errorf("key and value must be non-empty")
    }

    return ctx.GetStub().PutState(key, []byte(value))
}

// ReadData reads a key's value from the ledger
func (s *SecureContract) ReadData(ctx contractapi.TransactionContextInterface, key string) (string, error) {
    if key == "" {
        return "", fmt.Errorf("key must be non-empty")
    }

    data, err := ctx.GetStub().GetState(key)
    if err != nil {
        return "", fmt.Errorf("failed to read key %s: %v", key, err)
    }

    if data == nil {
        return "", fmt.Errorf("no data found for key: %s", key)
    }

    return string(data), nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(new(SecureContract))
    if err != nil {
        fmt.Printf("❌ Error creating chaincode: %s\n", err.Error())
        return
    }

    if err := chaincode.Start(); err != nil {
        fmt.Printf("❌ Error starting chaincode: %s\n", err.Error())
    }
}
