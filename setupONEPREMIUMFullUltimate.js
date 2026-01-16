// setupONEPREMIUMFullUltimate.js
// Node.js >=18 required. Run once in an empty GitHub repo: node setupONEPREMIUMFullUltimate.js

import fs from "fs";
import path from "path";
import fetch from "node-fetch";

const baseDir = process.cwd();

// ------------------- 1️⃣ CREATE FOLDERS -------------------
const folders = ["public","scripts","dao",".github/workflows"];
folders.forEach(folder=>{
  const p = path.join(baseDir,folder);
  if(!fs.existsSync(p)) fs.mkdirSync(p,{recursive:true});
});

// ------------------- 2️⃣ CONFIG -------------------
const configContent = `export const config = {
  etherscanApiKey: "K7NFZ3QVDRHN2GGB9T8CB8IX3FNQA1928E",
  contractAddress: "0xE430b07F7B168E77b07b29482DbF89EafA53f484",
  dex:{
    uniswap:"https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    sushiswap:"https://api.thegraph.com/subgraphs/name/sushiswap/exchange",
    oneinch:"https://api.1inch.io/v5.0/1/tokens",
    balancer:"https://api.balancer.fi/v2/pools"
  },
  walletTrackers:[
    "https://tokenlists.org/assets.json",
    "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/ethereum/assets/"
  ],
  logoUrl:"https://onepremium.de/assets/opm-logo",
  website:"https://onepremium.de",
  explorer:"https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484"
};`;
fs.writeFileSync(path.join(baseDir,"scripts/config.js"),configContent);

// ------------------- 3️⃣ UPDATE DATA -------------------
const updateDataContent = `import fs from "fs";
import fetch from "node-fetch";
import { config } from "./config.js";

async function fetchJSON(url){ try{ return await fetch(url).then(r=>r.json()) }catch(e){ return {error:"failed"} } }

async function updateHolders(){
  const url=\`https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress=\${config.contractAddress}&apikey=\${config.etherscanApiKey}\`;
  const data=await fetchJSON(url);
  fs.writeFileSync("public/holders.json",JSON.stringify(data,null,2));
}

async function updateDEXs(){
  const dexData={};
  for(const [name,url] of Object.entries(config.dex)){
    dexData[name]=await fetchJSON(url);
  }
  fs.writeFileSync("public/liquidity.json",JSON.stringify(dexData,null,2));
}

async function updateSecurity(){
  const url="https://solidityscan.com/quickscan/0xE430b07F7B168E77b07b29482DbF89EafA53f484/etherscan/mainnet?ref=etherscan";
  const data=await fetchJSON(url);
  fs.writeFileSync("public/security.json",JSON.stringify({snippet:JSON.stringify(data).slice(0,500)},null,2));
}

async function updateWallets(){
  const wallets={};
  for(const url of config.walletTrackers){
    wallets[url]=await fetchJSON(url);
  }
  fs.writeFileSync("public/wallets.json",JSON.stringify(wallets,null,2));
}

(async()=>{
  console.log("✅ Updating OPM Ultimate Data...");
  await updateHolders();
  await updateDEXs();
  await updateSecurity();
  await updateWallets();
  console.log("✅ All data updated successfully!");
})();`;
fs.writeFileSync(path.join(baseDir,"scripts/updateData.js"),updateDataContent);

// ------------------- 4️⃣ SEARCH INDEX -------------------
const searchIndexContent = `import fs from "fs";
import { config } from "./config.js";

const searchIndex=[
  {
    keyword:"OnePremium",
    symbol:"OPM",
    contract:config.contractAddress,
    website:config.website,
    explorer:config.explorer,
    logo:config.logoUrl,
    dex:["Uniswap","Sushiswap","1inch","Balancer"],
    wallets:["MetaMask","TrustWallet","TokenLists"]
  }
];

fs.writeFileSync("public/search-index.json",JSON.stringify(searchIndex,null,2));
console.log("✅ Search index ready!");`;
fs.writeFileSync(path.join(baseDir,"scripts/searchIndexBuilder.js"),searchIndexContent);

// ------------------- 5️⃣ DASHBOARD -------------------
const dashboardContent = `<!DOCTYPE html>
<html>
<head>
<title>OnePremium OPM Dashboard</title>
<style>
body{font-family:sans-serif;background:#f5f5f5;padding:20px}
h1{color:#2c3e50}
.badge{display:inline-block;padding:10px 20px;margin:10px;background:#eee;border-radius:5px;font-weight:bold;}
</style>
</head>
<body>
<h1>OnePremium (OPM) Transparency Dashboard</h1>
<div id="holders" class="badge">Holders: Loading...</div>
<div id="liquidity" class="badge">DEX Data: Loading...</div>
<div id="security" class="badge">Security: Loading...</div>
<div id="wallets" class="badge">Wallets: Loading...</div>
<script>
async function loadData(){
  const holders=await fetch("holders.json").then(r=>r.json());
  const liquidity=await fetch("liquidity.json").then(r=>r.json());
  const security=await fetch("security.json").then(r=>r.json());
  const wallets=await fetch("wallets.json").then(r=>r.json());
  const searchIndex=await fetch("search-index.json").then(r=>r.json());

  document.getElementById("holders").innerText="Holders: "+(holders.result?.length||"N/A");
  document.getElementById("liquidity").innerText="DEXs: "+Object.keys(liquidity).join(", ");
  document.getElementById("security").innerText="Security snippet: "+(security.snippet||"N/A");
  document.getElementById("wallets").innerText="Wallets: "+Object.keys(wallets).map(w=>w.split("/").pop()).join(", ");
}
loadData();
</script>
</body>
</html>`;
fs.writeFileSync(path.join(baseDir,"public/dashboard.html"),dashboardContent);

// ------------------- 6️⃣ DAO -------------------
const daoContent = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
contract OPMLiteGovernance is ERC20, GovernorSettings {
  constructor() ERC20("OnePremium Governance","OPMG") GovernorSettings(1,100,1e18){
    _mint(msg.sender,10000*10**18);
  }
}`;
fs.writeFileSync(path.join(baseDir,"dao/governance.sol"),daoContent);

// ------------------- 7️⃣ TOKEN JSON -------------------
const tokenJsonContent = `{
"name":"OnePremium",
"symbol":"OPM",
"contract":"0xE430b07F7B168E77b07b29482DbF89EafA53f484",
"decimals":18,
"logo":"https://onepremium.de/assets/opm-logo",
"website":"https://onepremium.de",
"explorer":"https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484"
}`;
fs.writeFileSync(path.join(baseDir,"public/token.json"),tokenJsonContent);

// ------------------- 8️⃣ GITHUB ACTIONS -------------------
const workflowContent = `name: OPM Ultimate Auto Update
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
        with: node-version:18
      - run: npm install node-fetch
      - run: node scripts/updateData.js
      - run: node scripts/searchIndexBuilder.js`;
fs.writeFileSync(path.join(baseDir,".github/workflows/update.yml"),workflowContent);

console.log("✅ ONEPREMIUM-OPM Ultimate full autonomous repo created with multi-DEX, wallet tracking, dashboard, badges, search-index, and GitHub Actions!");
