#!/usr/bin/env node
import { Command } from 'commander';
import compile from './lib/compile.js';
import fullsetup from './lib/fullsetup.js';
import deploy from './lib/deploy.js';
import fund from './lib/fund.js';
import sign from './lib/sign.js';
import recover from './lib/recover.js';
import deploySigreplayVuln from './lib/deploy-sigreplay-vuln.js';
import launchReentrancyAttack from './lib/launch-reentrancy-attack.js';
import deployReentrancyVuln from "./lib/deploy-reentrancy-vuln.js";
import launchSigReplayAttack from "./lib/launch-sigreplay-attack.js";

const program = new Command();

program.name("walletlab").description("CLI Wallet Lab").version("1.0.0");

program.command("compile").description("Compile contracts").action(compile);
program.command("fullsetup").description("Wallet + Deploy + TX").action(fullsetup);
program.command("deploy").description("Deploy multisig only").action(deploy);
program.command("deploy-sigreplay-vuln").description("Deploy vulnerable & attack contracts").action(deploySigreplayVuln);
program.command("deploy-reentrancy-vuln").description("Deploy vulnerable & attack contracts").action(deployReentrancyVuln);
program.command("launch-reentrancy-attack").description("Trigger the reentrancy exploit").option("--attack <address>").action(launchReentrancyAttack);
program.command("launch-sigreplay-attack").description("Trigger the sigreplay exploit").option("--attack <address>").action(launchSigReplayAttack);
program.command("recover").description("Recover wallet").option("--mnemonic <mnemonic>").option("--showBalance").action(recover);

program
    .command("fund")
    .description("Fund wallet")
    .argument("<address>")
    .option("--amount <eth>", "ETH amount", "5")
    .action(fund);

program
    .command("sign")
    .description("Sign/send TX manually")
    .option("--to <address>").option("--value <eth>").option("--privkey <hex>")
    .action(sign);

program.parse();
