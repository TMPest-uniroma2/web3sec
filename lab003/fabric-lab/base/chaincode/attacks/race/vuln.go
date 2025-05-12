package main

import (
    "fmt"
    "strconv"

    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type RaceContract struct {
    contractapi.Contract
}

// InitLedger initializes two accounts with 100 each
func (rc *RaceContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
    ctx.GetStub().PutState("Alice", []byte("100"))
    ctx.GetStub().PutState("Bob", []byte("100"))
    return nil
}

func (rc *RaceContract) Transfer(ctx contractapi.TransactionContextInterface, from, to string, amountStr string) error {
    amount, err := strconv.Atoi(amountStr)
    if err != nil {
        return fmt.Errorf("invalid amount: %v", err)
    }

    fromBytes, err := ctx.GetStub().GetState(from)
    if err != nil {
        return fmt.Errorf("cannot read 'from' balance: %v", err)
    }

    toBytes, err := ctx.GetStub().GetState(to)
    if err != nil {
        return fmt.Errorf("cannot read 'to' balance: %v", err)
    }

    fromBal, _ := strconv.Atoi(string(fromBytes))
    toBal, _ := strconv.Atoi(string(toBytes))

    if fromBal < amount {
        return fmt.Errorf("insufficient funds")
    }

    // Race condition: no MVCC conflict if TXs read same state version
    ctx.GetStub().PutState(from, []byte(strconv.Itoa(fromBal - amount)))
    ctx.GetStub().PutState(to, []byte(strconv.Itoa(toBal + amount)))
    return nil
}
