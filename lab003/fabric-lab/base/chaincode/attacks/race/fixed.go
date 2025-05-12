package main

import (
    "fmt"
    "strconv"

    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SafeContract struct {
    contractapi.Contract
}

func (sc *SafeContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
    ctx.GetStub().PutState("Alice", []byte("100"))
    ctx.GetStub().PutState("Bob", []byte("100"))
    return nil
}

func (sc *SafeContract) Transfer(ctx contractapi.TransactionContextInterface, from, to string, amountStr string) error {
    amount, err := strconv.Atoi(amountStr)
    if err != nil || amount <= 0 {
        return fmt.Errorf("invalid amount")
    }

    fromBytes, err := ctx.GetStub().GetState(from)
    if err != nil {
        return fmt.Errorf("cannot read sender state: %v", err)
    }
    toBytes, err := ctx.GetStub().GetState(to)
    if err != nil {
        return fmt.Errorf("cannot read recipient state: %v", err)
    }

    if fromBytes == nil || toBytes == nil {
        return fmt.Errorf("account not found")
    }

    fromBal, err := strconv.Atoi(string(fromBytes))
    if err != nil {
        return fmt.Errorf("invalid from balance")
    }
    toBal, err := strconv.Atoi(string(toBytes))
    if err != nil {
        return fmt.Errorf("invalid to balance")
    }

    if fromBal < amount {
        return fmt.Errorf("insufficient funds")
    }

    newFromBal := fromBal - amount
    newToBal := toBal + amount

    err = ctx.GetStub().PutState(from, []byte(strconv.Itoa(newFromBal)))
    if err != nil {
        return fmt.Errorf("failed to update sender balance: %v", err)
    }

    err = ctx.GetStub().PutState(to, []byte(strconv.Itoa(newToBal)))
    if err != nil {
        return fmt.Errorf("failed to update recipient balance: %v", err)
    }

    return nil
}
