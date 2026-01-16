# OnePremium (OPM) — Ethereum Utility Token

![OPM Logo](https://onepremium.de/assets/opm-logo)

**OnePremium (OPM)** is a high-security ERC-20 token deployed on Ethereum mainnet.  
This repository provides a full **transparency dashboard**, **auto-updating metrics**, **DAO governance skeleton**, and a **CoinMarketCap / CoinGecko submission-ready package**.

---

## 🔹 Project Overview

**Purpose:** OPM is designed to reward users for engagement in the OnePremium ecosystem.  
**Token Standard:** ERC-20  
**Blockchain:** Ethereum Mainnet  
**Total Supply:** 10,000 OPM  
**Decimals:** 18  

**Official Website:** [https://onepremium.de](https://onepremium.de)  
**Etherscan:** [OPM Token](https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484)  

---

## 🔹 Features

1. **Transparency Dashboard**  
   - Live holder count  
   - Liquidity snapshots  
   - Security audit snippets  
   - Auto-updating every 15 minutes via GitHub Actions

2. **Wallet Integration**  
   - MetaMask, TrustWallet, Coinbase Wallet compatible  
   - Add Token → Custom Token → Paste contract address  

3. **DEX & Market Visibility**  
   - [Uniswap V3 Token Page](https://app.uniswap.org/explore/tokens/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484)  
   - [DEX CoinMarketCap](https://dex.coinmarketcap.com/token/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484/)

4. **Automated Scripts**  
   - `/scripts/config.js` → stores all configuration (API keys, contract, URLs)  
   - `/scripts/updateData.js` → fetches holders, liquidity, security, and updates JSON files  

5. **DAO Governance Skeleton**  
   - ERC-20 governance contract (`dao/governance.sol`) ready for proposals, voting, and treasury management  

6. **Security & Audit**  
   - Verified contract on Etherscan  
   - QuickScan Security: [SolidityScan QuickScan](https://solidityscan.com/quickscan/0xE430b07F7B168E77b07b29482DbF89EafA53f484/etherscan/mainnet?ref=etherscan)  
   - Auto-updating security status via scripts  

7. **Auto-Updating Badges**  
   - Holders count  
   - Liquidity snapshot  
   - Security status  
   - Fully integrated in dashboard and JSON outputs  

---

## 🔹 Public Dashboard

**File:** `public/dashboard.html`  

**Features:**  
- Displays live metrics from JSON files  
- Badge-style indicators for holders, liquidity, security  
- Auto-refresh every 15 minutes via GitHub Actions

**Deployable:**  
- Vercel / Netlify / GitHub Pages  

**Sample Badge Display:**
```html
<img src="https://img.shields.io/badge/Holders-<HOLDER_COUNT>-blue"/>
<img src="https://img.shields.io/badge/Liquidity-<LIQUIDITY>-green"/>
<img src="https://img.shields.io/badge/Security-Passed-brightgreen"/>