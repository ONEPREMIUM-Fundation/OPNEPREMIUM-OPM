import fs from 'fs';
import path from 'path';

const baseDir = process.cwd();

// 1️⃣ Folders
const folders = [
  'public',
  'scripts',
  'contracts',
  'dao',
  '.github/workflows'
];

// 2️⃣ Files content
const files = {

  // README
  'README.md': `# OnePremium (OPM) — Ethereum Utility Token
![OPM Logo](https://onepremium.de/assets/opm-logo)

Official repository for OnePremium (OPM). Contains dashboard, DAO governance, auto-updating data, and submission package.

## Token Metadata
- Contract: 0xE430b07F7B168E77b07b29482DbF89EafA53f484
- Total Supply: 10,000 OPM
- Holders: Auto-updating
- Etherscan: https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484

## Dashboard
- public/dashboard.html (live holder, liquidity, security data)

## DAO Governance
- dao/governance.sol (ERC20 governance skeleton)

## Automated Scripts
- scripts/config.js
- scripts/updateData.js
`,

  // Whitepaper
  'whitepaper.md': `# OnePremium (OPM) — Whitepaper
## Overview
Utility ERC-20 token with platform rewards.

## Token Details
- Contract: 0xE430b07F7B168E77b07b29482DbF89EafA53f484
- Supply: 10,000 OPM
- Decimals: 18

## Sales
Public, Private, Seed with vesting schedules.

## Security
QuickScan verified. Full audit recommended.

## Disclaimer
Utility token only. No equity or governance rights.
`,

  // LICENSE
  'LICENSE': `MIT License
Copyright (c) 2026 OnePremium
Permission is hereby granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY.
`,

  // Config
  'scripts/config.js': `export const config = {
  etherscanApiKey: "K7NFZ3QVDRHN2GGB9T8CB8IX3FNQA1928E",
  contractAddress: "0xE430b07F7B168E77b07b29482DbF89EafA53f484",
  dexCMC: "https://dex.coinmarketcap.com/token/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484/",
  uniswap: "https://app.uniswap.org/explore/tokens/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484",
  logoUrl: "https://onepremium.de/assets/opm-logo"
};`,

  // Update data script
  'scripts/updateData.js': `import fetch from "node-fetch";
import { config } from "./config.js";
import fs from "fs";

async function fetchHolders() {
  const url = \`https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress=\${config.contractAddress}&apikey=\${config.etherscanApiKey}\`;
  const res = await fetch(url);
  const data = await res.json();
  fs.writeFileSync("public/holders.json", JSON.stringify(data, null, 2));
}

async function fetchLiquidity() {
  const res = await fetch(config.uniswap);
  const text = await res.text();
  fs.writeFileSync("public/liquidity.json", JSON.stringify({html: text.slice(0,500)}, null, 2));
}

async function fetchSecurity() {
  const url = "https://solidityscan.com/quickscan/0xE430b07F7B168E77b07b29482DbF89EafA53f484/etherscan/mainnet?ref=etherscan";
  const res = await fetch(url);
  const text = await res.text();
  fs.writeFileSync("public/security.json", JSON.stringify({html: text.slice(0,500)}, null, 2));
}

(async () => {
  console.log("Updating OPM data...");
  await fetchHolders();
  await fetchLiquidity();
  await fetchSecurity();
  console.log("Data updated.");
})();`,

  // Dashboard HTML
  'public/dashboard.html': `<!DOCTYPE html>
<html>
<head>
<title>OnePremium OPM Dashboard</title>
<style>body{font-family:sans-serif} .badge{display:inline-block;padding:10px;margin:5px;background:#eee;border-radius:5px}</style>
</head>
<body>
<h1>OnePremium (OPM) Transparency Dashboard</h1>
<div id="holders" class="badge">Holders: Loading...</div>
<div id="liquidity" class="badge">Liquidity: Loading...</div>
<div id="security" class="badge">Security: Loading...</div>
<script>
async function loadData() {
  const holders = await fetch("holders.json").then(r=>r.json());
  const liquidity = await fetch("liquidity.json").then(r=>r.json());
  const security = await fetch("security.json").then(r=>r.json());
  document.getElementById("holders").innerText = "Holders: " + (holders.result?.length || "N/A");
  document.getElementById("liquidity").innerText = "Liquidity snippet: " + (liquidity.html || "N/A");
  document.getElementById("security").innerText = "Security snippet: " + (security.html || "N/A");
}
loadData();
</script>
</body>
</html>`,

  // DAO skeleton
  'dao/governance.sol': `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";

contract OPMLiteGovernance is ERC20, GovernorSettings {
    constructor() ERC20("OnePremium Governance", "OPMG") GovernorSettings(1, 100, 1e18) {
        _mint(msg.sender, 10000 * 10**18);
    }
}`,

  // CoinMarketCap / CoinGecko package
  'public/token.json': `{
  "name": "OnePremium",
  "symbol": "OPM",
  "contract": "0xE430b07F7B168E77b07b29482DbF89EafA53f484",
  "decimals": 18,
  "logo": "https://onepremium.de/assets/opm-logo",
  "website": "https://onepremium.de",
  "explorer": "https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484"
}`
};

// 3️⃣ GitHub Workflow
files['.github/workflows/update.yml'] = `name: OPM Full Data Update
on:
  schedule:
    - cron: '*/15 * * * *'
  workflow_dispatch:
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm install node-fetch
      - run: node scripts/updateData.js`;

// 4️⃣ Create folders
folders.forEach(folder=>{
  const p = path.join(baseDir, folder);
  if(!fs.existsSync(p)) fs.mkdirSync(p, {recursive:true});
});

// 5️⃣ Write files
for(const [fp, content] of Object.entries(files)){
  const fullPath = path.join(baseDir, fp);
  const dir = path.dirname(fullPath);
  if(!fs.existsSync(dir)) fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(fullPath, content.trim());
}

console.log("✅ ONEPREMIUM-OPM full repository structure created successfully!");
