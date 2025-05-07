import { expect } from "chai";
import { ethers } from "ethers";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

describe("SimpleMultiSig", function () {
    let provider, signer0, signer1, signer2, recipient, contract, abi, bytecode;

    before(async () => {
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);

        abi = JSON.parse(fs.readFileSync(path.join(__dirname, "../artifacts/SimpleMultiSigABI.json")));
        bytecode = fs.readFileSync(path.join(__dirname, "../artifacts/SimpleMultiSigBytecode.txt"), "utf8");

        provider = new ethers.JsonRpcProvider("http://ganache:8545");
        const accounts = await provider.listAccounts();
        signer0 = await provider.getSigner(0);
        signer1 = await provider.getSigner(1);
        signer2 = await provider.getSigner(2);
        recipient = await provider.getSigner(3);

        const factory = new ethers.ContractFactory(abi, bytecode, signer0);
        contract = await factory.deploy([signer0.address, signer1.address, signer2.address], 2);

        await contract.waitForDeployment();

        await signer0.sendTransaction({
            to: await contract.getAddress(),
            value: ethers.parseEther("10")
        });
    });

    it("should submit and confirm a transaction", async () => {
        const tx = await contract.submitTransaction(recipient, ethers.parseEther("1"), {from: signer0.address});
        await tx.wait();
        const txData = await contract.transactions(0);
        expect(txData.destination).to.equal(recipient.address);
        expect(txData.confirmations).to.be.a('bigint');
        expect(txData.confirmations === 1n).to.be.true;
    });

    it("should execute after 2 confirmations", async () => {
        const balanceBefore = await provider.getBalance(recipient);
        const tx = await contract.connect(signer1).confirmTransaction(0);
        await tx.wait();
        const balanceAfter = await provider.getBalance(recipient);
        expect(balanceAfter - balanceBefore).to.equal(ethers.parseEther("1"));
    });
});
