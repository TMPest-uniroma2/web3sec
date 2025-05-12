package main

import (
    "fmt"
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type VulnerableContract struct {
    contractapi.Contract
}

func (vc *VulnerableContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
    return nil
}

func (vc *VulnerableContract) WriteData(ctx contractapi.TransactionContextInterface, key string, value string) error {
    return ctx.GetStub().PutState(key, []byte(value))
}

func (vc *VulnerableContract) ReadData(ctx contractapi.TransactionContextInterface, key string) (string, error) {
    data, err := ctx.GetStub().GetState(key)
    if err != nil {
        return "", err
    }
    if data == nil {
        return "", fmt.Errorf("no data found for key: %s", key)
    }
    return string(data), nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(new(VulnerableContract))
    if err != nil {
        fmt.Printf("Error create vuln chaincode: %s", err.Error())
        return
    }

    if err := chaincode.Start(); err != nil {
        fmt.Printf("Error starting vuln chaincode: %s", err.Error())
    }
}
