import fs from 'fs';
import path from 'path';
import solc from 'solc';

const compile = () => {
    const contracts = [
        { file: 'SimpleMultiSig.sol', name: 'SimpleMultiSig' },
        { file: 'attacks/reentrancy/Vulnerable.sol', name: 'Vulnerable2Reentrancy' },
        { file: 'attacks/reentrancy/ReentrancyAttack.sol', name: 'ReentrancyAttack' },
        { file: 'attacks/reentrancy/Fixed.sol', name: 'FixedReentrancy' },
        { file: 'attacks/sigreplay/Vulnerable.sol', name: 'Vulnerable2Sigreplay' },
        { file: 'attacks/sigreplay/Fixed.sol', name: 'FixedSigreplay' }
    ];

    for (const { file, name } of contracts) {
        console.log(`⏳ Compiling '${file}':${name}`)

        const source = fs.readFileSync(`./contracts/${file}`, 'utf8');

        const input = {
            language: 'Solidity',
            sources: {
                [file]: {
                    content: source
                }
            },
            settings: {
                optimizer: {
                    enabled: true,
                    runs: 200  // You can tweak this for contract usage pattern
                },
                outputSelection: {
                    '*': {
                        '*': ['abi', 'evm.bytecode.object']
                    }
                }
            }
        };

        const output = JSON.parse(solc.compile(JSON.stringify(input)));
        // console.log(output.contracts)

        const compiledContracts = output.contracts[file];
        if (!compiledContracts) {
            console.error(`❌ Compilation failed for ${file}. Check imports and syntax.`);
            continue;
        }

        for (const contractName in compiledContracts) {
            const contract = compiledContracts[contractName];
            fs.writeFileSync(`./artifacts/${contractName}ABI.json`, JSON.stringify(contract.abi, null, 2));
            fs.writeFileSync(`./artifacts/${contractName}Bytecode.txt`, contract.evm.bytecode.object);
            console.log(`✅ ${contractName} compiled`);
        }
    }
};

export default compile;
