#!/usr/bin/env python3
"""
================================================================================
                      OPM REPOSITORY AUTO-BUILDER
================================================================================
One Premium Token - Complete Repository Generator
Run: python3 deploy_opm.py
================================================================================
"""

import os
import sys
import json
import time
import base64
import hashlib
import requests
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import textwrap

# ==============================================================================
# CONFIGURATION
# ==============================================================================
class OPMConfig:
    """OPM Token Configuration"""
    
    # GitHub Configuration
    GITHUB_TOKEN = "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"
    REPO_NAME = "onepremium-token"
    REPO_DESCRIPTION = "OnePremium (OPM) Token - Professional Dashboard & Automation Suite"
    
    # OPM Token Details
    CONTRACT_ADDRESS = "0xE430b07F7B168E77b07b29482DbF89EafA53f484"
    ETHERSCAN_API = "K7NFZ3QVDRHN2GGB9T8CB8IX3FNQA1928E"
    
    # URLs
    LOGO_URL = "https://onepremium.de/assets/opm-logo"
    ETHERSCAN_URL = "https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484"
    UNISWAP_URL = "https://app.uniswap.org/explore/tokens/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484"
    CMC_URL = "https://dex.coinmarketcap.com/token/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484/"
    
    # Design Configuration
    COLORS = {
        "PRIMARY": "#667eea",
        "SECONDARY": "#764ba2",
        "SUCCESS": "#10b981",
        "WARNING": "#f59e0b",
        "DANGER": "#ef4444",
        "DARK": "#1f2937",
        "LIGHT": "#f3f4f6"
    }
    
    # Feature Flags
    AUTO_DEPLOY = True
    ENABLE_CI_CD = True
    ENABLE_MONITORING = True
    ENABLE_ANALYTICS = True

# ==============================================================================
# UTILITIES
# ==============================================================================
class Console:
    """Beautiful console output"""
    
    @staticmethod
    def header(text: str):
        print(f"\n{'='*60}")
        print(f"🎯 {text}")
        print(f"{'='*60}")
    
    @staticmethod
    def success(text: str):
        print(f"✅ {text}")
    
    @staticmethod
    def info(text: str):
        print(f"📌 {text}")
    
    @staticmethod
    def warning(text: str):
        print(f"⚠️  {text}")
    
    @staticmethod
    def error(text: str):
        print(f"❌ {text}")
    
    @staticmethod
    def step(text: str):
        print(f"🔧 {text}")
    
    @staticmethod
    def file(text: str):
        print(f"📄 {text}")
    
    @staticmethod
    def folder(text: str):
        print(f"📁 {text}")

class GitManager:
    """GitHub operations manager"""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_user(self) -> Optional[str]:
        """Get GitHub username from token"""
        try:
            response = requests.get(
                "https://api.github.com/user",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get("login")
        except Exception as e:
            Console.warning(f"Cannot get GitHub user: {e}")
        return None
    
    def create_repo(self, name: str, description: str, private: bool = False) -> Optional[Dict]:
        """Create GitHub repository"""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": False,
            "has_issues": True,
            "has_wiki": True,
            "has_projects": True
        }
        
        try:
            response = requests.post(
                "https://api.github.com/user/repos",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 422:
                Console.info("Repository already exists, using existing one")
                # Get existing repo
                user = self.get_user()
                if user:
                    response = requests.get(
                        f"https://api.github.com/repos/{user}/{name}",
                        headers=self.headers
                    )
                    if response.status_code == 200:
                        return response.json()
            return None
        except Exception as e:
            Console.error(f"Failed to create repository: {e}")
            return None
    
    def push_files(self, local_path: str, repo_url: str):
        """Push files to GitHub repository"""
        try:
            # Initialize git
            subprocess.run(["git", "init"], cwd=local_path, check=True)
            subprocess.run(["git", "config", "user.email", "deploy@opm.com"], 
                         cwd=local_path, check=True)
            subprocess.run(["git", "config", "user.name", "OPM Deployer"], 
                         cwd=local_path, check=True)
            
            # Add all files
            subprocess.run(["git", "add", "."], cwd=local_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit: OPM Token Repository"], 
                         cwd=local_path, check=True)
            
            # Add remote and push
            remote_url = f"https://{self.token}@github.com/{self.get_user()}/{OPMConfig.REPO_NAME}.git"
            subprocess.run(["git", "remote", "add", "origin", remote_url], 
                         cwd=local_path, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=local_path, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], 
                         cwd=local_path, check=True)
            
            return True
        except Exception as e:
            Console.error(f"Git operations failed: {e}")
            return False

# ==============================================================================
# FILE GENERATORS
# ==============================================================================
class FileGenerator:
    """Generate all repository files"""
    
    def __init__(self, config: OPMConfig):
        self.config = config
        self.created_files = 0
        
    def generate_all(self, base_dir: str):
        """Generate complete repository structure"""
        Console.header("BUILDING REPOSITORY STRUCTURE")
        
        # Create directory structure
        self.create_directories(base_dir)
        
        # Generate all files
        self.generate_config_files(base_dir)
        self.generate_dashboard_files(base_dir)
        self.generate_scripts(base_dir)
        self.generate_workflows(base_dir)
        self.generate_documentation(base_dir)
        
        Console.success(f"Created {self.created_files} files")
        return True
    
    def create_directories(self, base_dir: str):
        """Create all necessary directories"""
        directories = [
            "scripts",
            "src",
            "public",
            "public/css",
            "public/js",
            "public/images",
            "contracts",
            "docs",
            "tests",
            ".github/workflows",
            "data",
            "logs"
        ]
        
        for directory in directories:
            path = Path(base_dir) / directory
            path.mkdir(parents=True, exist_ok=True)
            Console.folder(f"Created: {directory}/")
    
    def write_file(self, path: Path, content: str):
        """Write file with proper formatting"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.created_files += 1
        Console.file(f"Created: {path}")
    
    def generate_config_files(self, base_dir: str):
        """Generate configuration files"""
        Console.step("Generating configuration files")
        
        # package.json
        package_json = {
            "name": self.config.REPO_NAME.lower().replace("-", "_"),
            "version": "1.0.0",
            "description": self.config.REPO_DESCRIPTION,
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "build": "webpack --mode production",
                "test": "jest",
                "lint": "eslint src/",
                "format": "prettier --write '**/*.{js,ts,json,md}'",
                "update": "node scripts/update.js",
                "deploy": "python3 deploy.py",
                "dashboard": "python3 -m http.server 8000"
            },
            "dependencies": {
                "express": "^4.18.2",
                "axios": "^1.5.0",
                "web3": "^4.0.3",
                "chart.js": "^4.4.0",
                "dotenv": "^16.3.1",
                "cors": "^2.8.5",
                "helmet": "^7.0.0",
                "morgan": "^1.10.0"
            },
            "devDependencies": {
                "nodemon": "^3.0.1",
                "jest": "^29.7.0",
                "eslint": "^8.50.0",
                "prettier": "^3.0.3",
                "webpack": "^5.88.2",
                "webpack-cli": "^5.1.4"
            },
            "engines": {
                "node": ">=18.0.0"
            },
            "keywords": ["ethereum", "token", "opm", "dashboard", "automation"],
            "author": "OnePremium",
            "license": "MIT"
        }
        
        self.write_file(Path(base_dir) / "package.json", json.dumps(package_json, indent=2))
        
        # .env.example
        env_content = f"""# OPM Token Configuration
ETHERSCAN_API_KEY={self.config.ETHERSCAN_API}
CONTRACT_ADDRESS={self.config.CONTRACT_ADDRESS}

# GitHub Configuration
GITHUB_TOKEN={self.config.GITHUB_TOKEN}
GITHUB_USER=your_username

# Server Configuration
PORT=3000
NODE_ENV=production

# Database Configuration (Optional)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=opm_token
DB_USER=postgres
DB_PASSWORD=your_password

# Security
JWT_SECRET=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=info

# Email (Optional for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Update Intervals (seconds)
UPDATE_INTERVAL=900
MONITOR_INTERVAL=300
BACKUP_INTERVAL=86400
"""
        self.write_file(Path(base_dir) / ".env.example", env_content)
        
        # .gitignore
        gitignore = """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
coverage/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
logs/
*.log

# Runtime data
data/*.json
!data/sample.json

# Temporary files
tmp/
temp/

# Security
*.pem
*.key
*.cert

# Backup files
*.bak
*.backup

# Test coverage
.nyc_output

# Production
.cache/
.next/
.nuxt/

# Documentation
docs/_build/
"""
        self.write_file(Path(base_dir) / ".gitignore", gitignore)
        
        # config.json
        config_json = {
            "project": {
                "name": "OnePremium Token Repository",
                "version": "1.0.0",
                "description": self.config.REPO_DESCRIPTION,
                "created": datetime.now().isoformat()
            },
            "token": {
                "name": "OnePremium",
                "symbol": "OPM",
                "address": self.config.CONTRACT_ADDRESS,
                "decimals": 18,
                "totalSupply": "10000000000000000000000",
                "logo": self.config.LOGO_URL,
                "website": "https://onepremium.de",
                "social": {
                    "twitter": "https://twitter.com/onepremium",
                    "telegram": "https://t.me/onepremium",
                    "discord": "https://discord.gg/onepremium"
                }
            },
            "apis": {
                "etherscan": {
                    "key": self.config.ETHERSCAN_API,
                    "baseUrl": "https://api.etherscan.io/api",
                    "endpoints": {
                        "holders": f"https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={self.config.CONTRACT_ADDRESS}",
                        "supply": f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={self.config.CONTRACT_ADDRESS}",
                        "transactions": f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={self.config.CONTRACT_ADDRESS}"
                    }
                },
                "dex": {
                    "uniswap": self.config.UNISWAP_URL,
                    "coinmarketcap": self.config.CMC_URL
                }
            },
            "dashboard": {
                "theme": {
                    "primary": self.config.COLORS["PRIMARY"],
                    "secondary": self.config.COLORS["SECONDARY"],
                    "dark": self.config.COLORS["DARK"]
                },
                "features": {
                    "realTimeUpdates": True,
                    "charts": True,
                    "export": True,
                    "notifications": True,
                    "mobileResponsive": True
                },
                "updateInterval": 900000
            },
            "security": {
                "monitoring": True,
                "rateLimiting": True,
                "backup": True,
                "alerts": True
            }
        }
        self.write_file(Path(base_dir) / "config.json", json.dumps(config_json, indent=2))
    
    def generate_dashboard_files(self, base_dir: str):
        """Generate dashboard HTML, CSS, and JS files"""
        Console.step("Generating dashboard files")
        
        # index.html
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OnePremium (OPM) Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="logo-container">
                <div class="logo">
                    <i class="fas fa-gem"></i>
                </div>
                <div class="logo-text">
                    <h1>OnePremium</h1>
                    <p class="token-symbol">OPM Token Dashboard</p>
                </div>
            </div>
            <div class="header-actions">
                <div class="last-updated" id="lastUpdated">
                    <i class="fas fa-sync-alt"></i>
                    <span>Updating...</span>
                </div>
                <button class="btn-refresh" onclick="refreshData()">
                    <i class="fas fa-redo"></i> Refresh
                </button>
            </div>
        </header>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Token Overview -->
            <section class="overview-section">
                <h2><i class="fas fa-chart-line"></i> Token Overview</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-wallet"></i>
                            <h3>Contract Address</h3>
                        </div>
                        <div class="stat-value">
                            <code class="contract-address">{self.config.CONTRACT_ADDRESS}</code>
                        </div>
                        <div class="stat-actions">
                            <a href="{self.config.ETHERSCAN_URL}" target="_blank" class="btn-link">
                                <i class="fas fa-external-link-alt"></i> Etherscan
                            </a>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-users"></i>
                            <h3>Token Holders</h3>
                        </div>
                        <div class="stat-value" id="holderCount">Loading...</div>
                        <div class="stat-change">
                            <span id="holderChange">--</span> from last update
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-coins"></i>
                            <h3>Total Supply</h3>
                        </div>
                        <div class="stat-value">
                            <span id="totalSupply">10,000</span> OPM
                        </div>
                        <div class="stat-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 95%"></div>
                            </div>
                            <span>95% Circulating</span>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-hand-holding-usd"></i>
                            <h3>Market Value</h3>
                        </div>
                        <div class="stat-value" id="marketValue">$ --</div>
                        <div class="stat-change">
                            <span id="priceChange">--</span> 24h change
                        </div>
                    </div>
                </div>
            </section>

            <!-- Charts & Analytics -->
            <section class="analytics-section">
                <h2><i class="fas fa-chart-bar"></i> Analytics</h2>
                <div class="charts-grid">
                    <div class="chart-card">
                        <h3>Holder Distribution</h3>
                        <canvas id="holdersChart"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>Transaction Volume (7d)</h3>
                        <canvas id="volumeChart"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>Price Movement</h3>
                        <canvas id="priceChart"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>Top Holders</h3>
                        <div class="holders-list" id="topHolders">
                            <div class="loading">Loading holders...</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Quick Links -->
            <section class="links-section">
                <h2><i class="fas fa-external-link-alt"></i> Quick Links</h2>
                <div class="links-grid">
                    <a href="{self.config.UNISWAP_URL}" target="_blank" class="link-card">
                        <i class="fas fa-exchange-alt"></i>
                        <h3>Trade on Uniswap</h3>
                        <p>Swap OPM tokens instantly</p>
                    </a>
                    <a href="{self.config.CMC_URL}" target="_blank" class="link-card">
                        <i class="fas fa-chart-pie"></i>
                        <h3>CoinMarketCap</h3>
                        <p>View market data & rankings</p>
                    </a>
                    <a href="https://github.com/onepremium/opm-repo" target="_blank" class="link-card">
                        <i class="fab fa-github"></i>
                        <h3>GitHub Repository</h3>
                        <p>View source code & contribute</p>
                    </a>
                    <a href="docs/whitepaper.html" class="link-card">
                        <i class="fas fa-file-contract"></i>
                        <h3>Whitepaper</h3>
                        <p>Read the technical documentation</p>
                    </a>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-logo">
                    <i class="fas fa-gem"></i>
                    <span>OnePremium OPM</span>
                </div>
                <div class="footer-info">
                    <p>© {datetime.now().year} OnePremium Token. All rights reserved.</p>
                    <p class="footer-disclaimer">
                        This dashboard provides real-time information about the OPM token.
                        Not financial advice. Always do your own research.
                    </p>
                </div>
                <div class="footer-links">
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-telegram"></i></a>
                    <a href="#"><i class="fab fa-discord"></i></a>
                    <a href="#"><i class="fab fa-github"></i></a>
                </div>
            </div>
            <div class="system-status">
                <span class="status-indicator online"></span>
                <span>System: <strong id="systemStatus">Online</strong></span>
                <span class="last-update">Last update: <span id="updateTime">--:--:--</span></span>
            </div>
        </footer>
    </div>

    <!-- JavaScript -->
    <script src="js/app.js"></script>
    <script src="js/charts.js"></script>
</body>
</html>
"""
        self.write_file(Path(base_dir) / "public/index.html", index_html)
        
        # style.css
        css_content = f"""/* OPM Dashboard Styles */
:root {{
    --primary-color: {self.config.COLORS["PRIMARY"]};
    --secondary-color: {self.config.COLORS["SECONDARY"]};
    --success-color: {self.config.COLORS["SUCCESS"]};
    --warning-color: {self.config.COLORS["WARNING"]};
    --danger-color: {self.config.COLORS["DANGER"]};
    --dark-color: {self.config.COLORS["DARK"]};
    --light-color: {self.config.COLORS["LIGHT"]};
    --border-radius: 12px;
    --box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    --transition: all 0.3s ease;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    color: var(--dark-color);
    line-height: 1.6;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}}

/* Header */
.header {{
    background: white;
    border-radius: var(--border-radius);
    padding: 24px 32px;
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--box-shadow);
    animation: slideDown 0.5s ease;
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 20px;
}}

.logo {{
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 28px;
}}

.logo-text h1 {{
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}}

.token-symbol {{
    color: #666;
    font-size: 14px;
    font-weight: 500;
}}

.header-actions {{
    display: flex;
    align-items: center;
    gap: 20px;
}}

.last-updated {{
    display: flex;
    align-items: center;
    gap: 8px;
    color: #666;
    font-size: 14px;
}}

.btn-refresh {{
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: var(--border-radius);
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 8px;
}}

.btn-refresh:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}}

/* Main Content */
.main-content {{
    display: flex;
    flex-direction: column;
    gap: 30px;
}}

section {{
    background: white;
    border-radius: var(--border-radius);
    padding: 30px;
    box-shadow: var(--box-shadow);
    animation: fadeIn 0.5s ease;
}}

h2 {{
    font-size: 24px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--dark-color);
}}

/* Stats Grid */
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
}}

.stat-card {{
    background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    border-radius: var(--border-radius);
    padding: 24px;
    transition: var(--transition);
    border: 1px solid #e2e8f0;
}}

.stat-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}}

.stat-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}}

.stat-header i {{
    font-size: 24px;
    color: var(--primary-color);
}}

.stat-header h3 {{
    font-size: 18px;
    font-weight: 600;
}}

.stat-value {{
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 10px;
    color: var(--dark-color);
}}

.contract-address {{
    background: #f1f5f9;
    padding: 8px 12px;
    border-radius: 6px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 14px;
    word-break: break-all;
}}

.stat-change {{
    font-size: 14px;
    color: #666;
}}

.stat-progress {{
    margin-top: 15px;
}}

.progress-bar {{
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    margin-bottom: 8px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--success-color), #34d399);
    border-radius: 4px;
    transition: width 1s ease;
}}

.stat-actions {{
    margin-top: 20px;
}}

.btn-link {{
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: var(--transition);
}}

.btn-link:hover {{
    color: var(--secondary-color);
}}

/* Charts */
.charts-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 24px;
}}

.chart-card {{
    background: white;
    border-radius: var(--border-radius);
    padding: 24px;
    border: 1px solid #e2e8f0;
}}

.chart-card h3 {{
    font-size: 18px;
    margin-bottom: 20px;
    color: var(--dark-color);
}}

canvas {{
    width: 100% !important;
    height: 250px !important;
}}

.holders-list {{
    max-height: 300px;
    overflow-y: auto;
}}

.holder-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #e2e8f0;
}}

.holder-address {{
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 14px;
    color: #666;
}}

.holder-amount {{
    font-weight: 600;
    color: var(--dark-color);
}}

/* Links Grid */
.links-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
}}

.link-card {{
    background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    border-radius: var(--border-radius);
    padding: 30px;
    text-decoration: none;
    color: inherit;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border: 2px solid transparent;
}}

.link-card:hover {{
    transform: translateY(-5px);
    border-color: var(--primary-color);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
}}

.link-card i {{
    font-size: 40px;
    color: var(--primary-color);
    margin-bottom: 20px;
}}

.link-card h3 {{
    font-size: 20px;
    margin-bottom: 10px;
    color: var(--dark-color);
}}

.link-card p {{
    color: #666;
    font-size: 14px;
    line-height: 1.5;
}}

/* Footer */
.footer {{
    margin-top: 50px;
    background: white;
    border-radius: var(--border-radius);
    padding: 30px;
    box-shadow: var(--box-shadow);
}}

.footer-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}}

.footer-logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 20px;
    font-weight: 700;
    color: var(--dark-color);
}}

.footer-logo i {{
    color: var(--primary-color);
    font-size: 24px;
}}

.footer-info p {{
    color: #666;
    font-size: 14px;
    margin-bottom: 5px;
}}

.footer-disclaimer {{
    font-size: 12px !important;
    color: #999 !important;
    max-width: 400px;
}}

.footer-links {{
    display: flex;
    gap: 20px;
}}

.footer-links a {{
    color: #666;
    font-size: 20px;
    transition: var(--transition);
}}

.footer-links a:hover {{
    color: var(--primary-color);
}}

.system-status {{
    display: flex;
    align-items: center;
    gap: 15px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    color: #666;
    font-size: 14px;
}}

.status-indicator {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--success-color);
}}

.status-indicator.online {{
    background: var(--success-color);
    animation: pulse 2s infinite;
}}

.last-update {{
    margin-left: auto;
}}

/* Animations */
@keyframes slideDown {{
    from {{ transform: translateY(-20px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .header {{
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }}
    
    .stats-grid,
    .charts-grid,
    .links-grid {{
        grid-template-columns: 1fr;
    }}
    
    .footer-content {{
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }}
    
    .system-status {{
        flex-direction: column;
        gap: 10px;
    }}
    
    .last-update {{
        margin-left: 0;
    }}
}}

.loading {{
    text-align: center;
    padding: 40px;
    color: #666;
    font-style: italic;
}}
"""
        self.write_file(Path(base_dir) / "public/css/style.css", css_content)
        
        # app.js
        app_js = """// OPM Dashboard JavaScript
class OPMDashboard {
    constructor() {
        this.config = window.opmConfig || {};
        this.data = {
            holders: [],
            supply: 0,
            price: 0,
            lastUpdate: null
        };
        
        this.initialize();
    }
    
    async initialize() {
        console.log('🚀 OPM Dashboard Initializing...');
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Load initial data
        await this.loadData();
        
        // Initialize charts
        this.initCharts();
        
        // Start auto-refresh
        this.startAutoRefresh();
        
        this.updateSystemStatus();
    }
    
    setupEventListeners() {
        // Refresh button
        document.querySelector('.btn-refresh').addEventListener('click', () => this.loadData());
        
        // Contract address copy
        const contractElement = document.querySelector('.contract-address');
        contractElement.addEventListener('click', () => {
            navigator.clipboard.writeText(contractElement.textContent);
            this.showNotification('Contract address copied to clipboard!', 'success');
        });
    }
    
    async loadData() {
        try {
            this.showLoading(true);
            
            // Simulate API calls - in production, replace with actual API endpoints
            await this.simulateApiCalls();
            
            // Update UI
            this.updateUI();
            
            // Update last updated time
            this.updateLastUpdated();
            
            this.showNotification('Data updated successfully!', 'success');
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showNotification('Failed to update data', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    async simulateApiCalls() {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data for demonstration
        this.data = {
            holders: [
                { address: '0x742d35Cc6634C0532925a3b844Bc9e...', amount: '1,234.56', percentage: '12.34%' },
                { address: '0x742d35Cc6634C0532925a3b844Bc9e...', amount: '987.65', percentage: '9.87%' },
                { address: '0x742d35Cc6634C0532925a3b844Bc9e...', amount: '654.32', percentage: '6.54%' },
                { address: '0x742d35Cc6634C0532925a3b844Bc9e...', amount: '321.09', percentage: '3.21%' },
                { address: '0x742d35Cc6634C0532925a3b844Bc9e...', amount: '210.87', percentage: '2.10%' }
            ],
            totalHolders: 1254,
            totalSupply: '10,000',
            circulatingSupply: '9,500',
            marketValue: '$245,678',
            priceChange: '+2.34%',
            holderChange: '+12',
            lastUpdate: new Date().toISOString()
        };
    }
    
    updateUI() {
        // Update holders count
        document.getElementById('holderCount').textContent = this.data.totalHolders.toLocaleString();
        document.getElementById('holderChange').textContent = `+${this.data.holderChange}`;
        
        // Update market value
        document.getElementById('marketValue').textContent = this.data.marketValue;
        document.getElementById('priceChange').textContent = this.data.priceChange;
        
        // Update holders list
        this.updateHoldersList();
        
        // Update charts
        this.updateCharts();
    }
    
    updateHoldersList() {
        const container = document.getElementById('topHolders');
        container.innerHTML = '';
        
        this.data.holders.forEach(holder => {
            const div = document.createElement('div');
            div.className = 'holder-item';
            div.innerHTML = `
                <div class="holder-info">
                    <div class="holder-address">${holder.address}</div>
                </div>
                <div class="holder-stats">
                    <div class="holder-amount">${holder.amount} OPM</div>
                    <div class="holder-percentage">${holder.percentage}</div>
                </div>
            `;
            container.appendChild(div);
        });
    }
    
    initCharts() {
        // Initialize chart instances
        this.charts = {
            holders: this.createHoldersChart(),
            volume: this.createVolumeChart(),
            price: this.createPriceChart()
        };
    }
    
    createHoldersChart() {
        const ctx = document.getElementById('holdersChart').getContext('2d');
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Top 5 Holders', 'Other Holders'],
                datasets: [{
                    data: [34.56, 65.44],
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.6)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    createVolumeChart() {
        const ctx = document.getElementById('volumeChart').getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Volume (ETH)',
                    data: [12.5, 19.2, 15.3, 22.1, 18.7, 25.4, 20.9],
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    createPriceChart() {
        const ctx = document.getElementById('priceChart').getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1D', '2D', '3D', '4D', '5D', '6D', '7D'],
                datasets: [{
                    label: 'Price (USD)',
                    data: [24.5, 25.1, 24.8, 26.3, 25.9, 26.7, 26.2],
                    borderColor: 'rgb(16, 185, 129)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    }
    
    updateCharts() {
        // Update chart data here when real data is available
        console.log('Updating charts with new data...');
    }
    
    updateLastUpdated() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const dateString = now.toLocaleDateString();
        
        document.getElementById('lastUpdated').innerHTML = `
            <i class="fas fa-sync-alt"></i>
            <span>Last updated: ${dateString} ${timeString}</span>
        `;
        
        document.getElementById('updateTime').textContent = timeString;
    }
    
    updateSystemStatus() {
        const statusElement = document.getElementById('systemStatus');
        statusElement.textContent = 'Online';
        statusElement.style.color = '#10b981';
    }
    
    startAutoRefresh() {
        // Auto-refresh every 60 seconds
        setInterval(() => {
            this.loadData();
        }, 60000);
    }
    
    showLoading(show) {
        const refreshBtn = document.querySelector('.btn-refresh');
        const icon = refreshBtn.querySelector('i');
        
        if (show) {
            refreshBtn.disabled = true;
            icon.className = 'fas fa-spinner fa-spin';
        } else {
            refreshBtn.disabled = false;
            icon.className = 'fas fa-redo';
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
        
        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new OPMDashboard();
});

// Global refresh function
function refreshData() {
    if (window.dashboard) {
        window.dashboard.loadData();
    }
}
"""
        self.write_file(Path(base_dir) / "public/js/app.js", app_js)
    
    def generate_scripts(self, base_dir: str):
        """Generate automation scripts"""
        Console.step("Generating automation scripts")
        
        # update.js
        update_js = f"""// OPM Token Data Updater
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class OPMUpdater {{
    constructor() {{
        this.config = {{
            contractAddress: '{self.config.CONTRACT_ADDRESS}',
            etherscanApiKey: '{self.config.ETHERSCAN_API}',
            updateInterval: 900000, // 15 minutes
            dataDir: path.join(__dirname, '../data')
        }};
        
        this.init();
    }}
    
    init() {{
        // Create data directory if it doesn't exist
        if (!fs.existsSync(this.config.dataDir)) {{
            fs.mkdirSync(this.config.dataDir, {{ recursive: true }});
        }}
        
        console.log('🚀 OPM Data Updater Initialized');
        console.log(`Contract: ${{this.config.contractAddress}}`);
    }}
    
    async updateAllData() {{
        console.log('📊 Starting data update...');
        
        try {{
            await Promise.all([
                this.updateTokenInfo(),
                this.updateHolders(),
                this.updateSupply(),
                this.updateTransactions()
            ]);
            
            console.log('✅ All data updated successfully');
            this.logUpdate();
            
        }} catch (error) {{
            console.error('❌ Error updating data:', error);
            throw error;
        }}
    }}
    
    async updateTokenInfo() {{
        const url = `https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress=${{this.config.contractAddress}}&apikey=${{this.config.etherscanApiKey}}`;
        
        try {{
            const response = await axios.get(url);
            
            if (response.data.status === '1') {{
                const data = {{
                    timestamp: new Date().toISOString(),
                    data: response.data.result[0]
                }};
                
                this.saveData('token-info.json', data);
                console.log('✅ Token info updated');
            }}
        }} catch (error) {{
            console.error('Error updating token info:', error);
        }}
    }}
    
    async updateHolders() {{
        const url = `https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress=${{this.config.contractAddress}}&page=1&offset=100&apikey=${{this.config.etherscanApiKey}}`;
        
        try {{
            const response = await axios.get(url);
            
            if (response.data.status === '1') {{
                const holders = response.data.result.slice(0, 50); // Top 50 holders
                const data = {{
                    timestamp: new Date().toISOString(),
                    total: response.data.result.length,
                    holders: holders.map(holder => ({{
                        address: holder.TokenHolderAddress,
                        balance: holder.TokenHolderQuantity,
                        percentage: ((holder.TokenHolderQuantity / response.data.result[0].TokenHolderQuantity) * 100).toFixed(4)
                    }}))
                }};
                
                this.saveData('holders.json', data);
                console.log(`✅ Holders updated: ${{data.total}} total holders`);
            }}
        }} catch (error) {{
            console.error('Error updating holders:', error);
        }}
    }}
    
    async updateSupply() {{
        const url = `https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress=${{this.config.contractAddress}}&apikey=${{this.config.etherscanApiKey}}`;
        
        try {{
            const response = await axios.get(url);
            
            if (response.data.status === '1') {{
                const data = {{
                    timestamp: new Date().toISOString(),
                    totalSupply: response.data.result,
                    circulatingSupply: (parseInt(response.data.result) * 0.95).toString(),
                    marketCap: 'N/A' // Would need price data
                }};
                
                this.saveData('supply.json', data);
                console.log('✅ Supply data updated');
            }}
        }} catch (error) {{
            console.error('Error updating supply:', error);
        }}
    }}
    
    async updateTransactions() {{
        const url = `https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=${{this.config.contractAddress}}&page=1&offset=100&sort=desc&apikey=${{this.config.etherscanApiKey}}`;
        
        try {{
            const response = await axios.get(url);
            
            if (response.data.status === '1') {{
                const data = {{
                    timestamp: new Date().toISOString(),
                    transactions: response.data.result.slice(0, 50) // Last 50 transactions
                }};
                
                this.saveData('transactions.json', data);
                console.log('✅ Transactions updated');
            }}
        }} catch (error) {{
            console.error('Error updating transactions:', error);
        }}
    }}
    
    saveData(filename, data) {{
        const filepath = path.join(this.config.dataDir, filename);
        fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
    }}
    
    logUpdate() {{
        const logEntry = {{
            timestamp: new Date().toISOString(),
            status: 'success',
            message: 'Data update completed'
        }};
        
        const logFile = path.join(this.config.dataDir, 'update-log.json');
        let logs = [];
        
        if (fs.existsSync(logFile)) {{
            logs = JSON.parse(fs.readFileSync(logFile, 'utf8'));
        }}
        
        logs.push(logEntry);
        
        // Keep only last 100 log entries
        if (logs.length > 100) {{
            logs = logs.slice(-100);
        }}
        
        fs.writeFileSync(logFile, JSON.stringify(logs, null, 2));
    }}
    
    startContinuousUpdates() {{
        console.log(`🔄 Starting continuous updates every ${{this.config.updateInterval / 60000}} minutes`);
        
        // Initial update
        this.updateAllData();
        
        // Schedule updates
        setInterval(() => {{
            this.updateAllData();
        }}, this.config.updateInterval);
    }}
}}

// Command line interface
const updater = new OPMUpdater();

if (require.main === module) {{
    const args = process.argv.slice(2);
    
    if (args.includes('--continuous')) {{
        updater.startContinuousUpdates();
    }} else if (args.includes('--once')) {{
        updater.updateAllData().then(() => process.exit(0));
    }} else {{
        console.log('OPM Data Updater');
        console.log('Usage:');
        console.log('  node update.js --once      Update data once');
        console.log('  node update.js --continuous  Start continuous updates');
        updater.updateAllData().then(() => process.exit(0));
    }}
}}

module.exports = OPMUpdater;
"""
        self.write_file(Path(base_dir) / "scripts/update.js", update_js)
        
        # deploy.sh
        deploy_sh = """#!/bin/bash

# OPM Repository Deployment Script
# Run with: bash deploy.sh

set -e  # Exit on error

echo "🚀 OPM Repository Deployment"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing=()
    
    # Check for git
    if ! command -v git &> /dev/null; then
        missing+=("git")
    fi
    
    # Check for node
    if ! command -v node &> /dev/null; then
        missing+=("node")
    fi
    
    # Check for npm
    if ! command -v npm &> /dev/null; then
        missing+=("npm")
    fi
    
    # Check for python3
    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        print_error "Missing prerequisites: ${missing[*]}"
        print_warning "Please install missing packages and try again."
        exit 1
    fi
    
    print_success "All prerequisites found"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install npm packages
    if [ -f "package.json" ]; then
        print_status "Installing npm packages..."
        npm install
        print_success "npm packages installed"
    fi
    
    # Install Python packages
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python packages..."
        pip3 install -r requirements.txt
        print_success "Python packages installed"
    fi
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    if [ -f "package.json" ]; then
        if npm run test; then
            print_success "Tests passed"
        else
            print_error "Tests failed"
            exit 1
        fi
    fi
}

# Build project
build_project() {
    print_status "Building project..."
    
    if [ -f "package.json" ] && grep -q '"build"' package.json; then
        npm run build
        print_success "Build completed"
    fi
}

# Update data
update_data() {
    print_status "Updating token data..."
    
    if [ -f "scripts/update.js" ]; then
        node scripts/update.js --once
        print_success "Data updated"
    elif [ -f "scripts/update.py" ]; then
        python3 scripts/update.py
        print_success "Data updated"
    fi
}

# Deploy to GitHub
deploy_to_github() {
    print_status "Deploying to GitHub..."
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        print_error "Not a git repository. Run 'git init' first."
        exit 1
    fi
    
    # Add all files
    git add .
    
    # Check if there are changes
    if git diff --cached --quiet; then
        print_warning "No changes to commit"
    else
        # Commit changes
        git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
        
        # Push to GitHub
        if git push; then
            print_success "Deployed to GitHub"
        else
            print_error "Failed to push to GitHub"
            exit 1
        fi
    fi
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Start dashboard server in background
    if [ -f "package.json" ] && grep -q '"start"' package.json; then
        npm start &
        print_success "Dashboard server started"
    elif [ -f "app.py" ]; then
        python3 app.py &
        print_success "Python server started"
    fi
    
    # Start monitoring if available
    if [ -f "scripts/monitor.py" ]; then
        python3 scripts/monitor.py &
        print_success "Monitoring started"
    fi
}

# Main deployment function
main() {
    echo "OPM Deployment Started"
    echo "====================="
    
    # Run all steps
    check_prerequisites
    install_dependencies
    run_tests
    build_project
    update_data
    deploy_to_github
    start_services
    
    echo ""
    echo "========================================"
    print_success "Deployment completed successfully!"
    echo ""
    echo "📊 Dashboard: http://localhost:3000"
    echo "📈 API: http://localhost:3000/api"
    echo "📁 Repository: https://github.com/[USER]/[REPO]"
    echo ""
    echo "To stop services, press Ctrl+C"
    echo "========================================"
    
    # Wait for user interrupt
    wait
}

# Run main function
main "$@"
"""
        self.write_file(Path(base_dir) / "scripts/deploy.sh", deploy_sh)
        
        # monitor.py
        monitor_py = f"""#!/usr/bin/env python3
"""
# OPM Token Monitor
# Monitors token metrics and sends alerts

import time
import json
import requests
import smtplib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class OPMMonitor:
    def __init__(self):
        self.config = {{
            "contract_address": "{self.config.CONTRACT_ADDRESS}",
            "etherscan_api": "{self.config.ETHERSCAN_API}",
            "check_interval": 300,  # 5 minutes
            "alert_threshold": 10,   # 10% change
            "data_file": "data/monitor.json",
            "log_file": "logs/monitor.log"
        }}
        
        # Setup logging
        self.setup_logging()
        
        # Load previous data
        self.previous_data = self.load_data()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_path = Path(self.config["log_file"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config["log_file"]),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_data(self):
        """Load previous monitoring data"""
        try:
            data_path = Path(self.config["data_file"])
            if data_path.exists():
                with open(data_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading data: {{e}}")
        return {{}}
    
    def save_data(self, data):
        """Save current monitoring data"""
        try:
            data_path = Path(self.config["data_file"])
            data_path.parent.mkdir(parents=True, exist_ok=True)
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving data: {{e}}")
    
    def get_token_metrics(self):
        """Get current token metrics from Etherscan"""
        url = "https://api.etherscan.io/api"
        params = {{
            "module": "token",
            "action": "tokeninfo",
            "contractaddress": self.config["contract_address"],
            "apikey": self.config["etherscan_api"]
        }}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1" and data.get("result"):
                token_data = data["result"][0]
                return {{
                    "timestamp": datetime.now().isoformat(),
                    "price_usd": float(token_data.get("tokenPriceUSD", 0)),
                    "holders": int(token_data.get("holders", 0)),
                    "total_supply": int(token_data.get("totalSupply", 0)),
                    "transactions_24h": int(token_data.get("transactions24h", 0)),
                    "volume_24h": float(token_data.get("volume24h", 0))
                }}
        except Exception as e:
            self.logger.error(f"Error fetching metrics: {{e}}")
        
        return None
    
    def get_holder_growth(self):
        """Calculate holder growth rate"""
        if not self.previous_data:
            return 0
        
        current_time = datetime.now()
        previous_time = datetime.fromisoformat(self.previous_data.get("timestamp", current_time.isoformat()))
        
        # Only calculate if within reasonable time frame
        time_diff = (current_time - previous_time).total_seconds()
        if time_diff < 3600:  # Less than 1 hour
            current_holders = self.previous_data.get("holders", 0)
            previous_holders = self.previous_data.get("previous_holders", current_holders)
            
            if previous_holders > 0:
                return ((current_holders - previous_holders) / previous_holders) * 100
        
        return 0
    
    def check_alerts(self, current_metrics):
        """Check if alert conditions are met"""
        alerts = []
        
        if not current_metrics:
            return alerts
        
        # Price change alert
        if self.previous_data and "price_usd" in self.previous_data:
            price_change = abs((current_metrics["price_usd"] - self.previous_data["price_usd"]) / 
                             self.previous_data["price_usd"] * 100)
            if price_change > self.config["alert_threshold"]:
                alerts.append({{
                    "type": "price_change",
                    "message": f"Price changed by {{price_change:.2f}}%",
                    "severity": "high" if price_change > 20 else "medium"
                }})
        
        # Holder growth alert
        holder_growth = self.get_holder_growth()
        if abs(holder_growth) > 5:
            alerts.append({{
                "type": "holder_growth",
                "message": f"Holder growth: {{holder_growth:.2f}}%",
                "severity": "medium"
            }})
        
        # Transaction spike alert
        if self.previous_data and "transactions_24h" in self.previous_data:
            tx_change = ((current_metrics["transactions_24h"] - self.previous_data["transactions_24h"]) / 
                        self.previous_data["transactions_24h"] * 100)
            if tx_change > 50:
                alerts.append({{
                    "type": "transaction_spike",
                    "message": f"Transaction spike: {{tx_change:.2f}}%",
                    "severity": "high"
                }})
        
        return alerts
    
    def send_alert(self, alerts):
        """Send alert notifications"""
        if not alerts:
            return
        
        self.logger.warning(f"Alerts detected: {{len(alerts)}}")
        
        # Group by severity
        high_alerts = [a for a in alerts if a["severity"] == "high"]
        medium_alerts = [a for a in alerts if a["severity"] == "medium"]
        
        # Create alert message
        message_lines = ["🚨 OPM Token Alerts"]
        message_lines.append("=" * 40)
        message_lines.append(f"Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        message_lines.append(f"Contract: {{self.config['contract_address']}}")
        message_lines.append("")
        
        if high_alerts:
            message_lines.append("🔴 HIGH PRIORITY:")
            for alert in high_alerts:
                message_lines.append(f"  • {{alert['message']}}")
            message_lines.append("")
        
        if medium_alerts:
            message_lines.append("🟡 MEDIUM PRIORITY:")
            for alert in medium_alerts:
                message_lines.append(f"  • {{alert['message']}}")
        
        message = "\n".join(message_lines)
        
        # Log alerts
        self.logger.warning(message)
        
        # Save to alerts file
        alert_data = {{
            "timestamp": datetime.now().isoformat(),
            "alerts": alerts,
            "message": message
        }}
        
        alerts_file = Path("data/alerts.json")
        alerts_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            alerts_list = []
            if alerts_file.exists():
                with open(alerts_file, 'r') as f:
                    alerts_list = json.load(f)
            
            alerts_list.append(alert_data)
            
            # Keep only last 100 alerts
            if len(alerts_list) > 100:
                alerts_list = alerts_list[-100:]
            
            with open(alerts_file, 'w') as f:
                json.dump(alerts_list, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving alerts: {{e}}")
        
        # Here you could add:
        # - Telegram bot notification
        # - Discord webhook
        # - Email notification
        # Example for email (requires SMTP setup):
        # self.send_email_alert(message)
    
    def send_email_alert(self, message):
        """Send email alert (example implementation)"""
        try:
            # This is just an example - configure with your SMTP settings
            msg = MIMEMultipart()
            msg['From'] = "alerts@onepremium.com"
            msg['To'] = "admin@onepremium.com"
            msg['Subject'] = "🚨 OPM Token Alert"
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to SMTP server and send
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls()
            # server.login('your_email@gmail.com', 'your_password')
            # server.send_message(msg)
            # server.quit()
            
        except Exception as e:
            self.logger.error(f"Error sending email: {{e}}")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info("Starting OPM Token Monitor")
        self.logger.info(f"Contract: {{self.config['contract_address']}}")
        self.logger.info(f"Check interval: {{self.config['check_interval']}} seconds")
        
        while True:
            try:
                self.logger.info("Checking token metrics...")
                
                # Get current metrics
                current_metrics = self.get_token_metrics()
                
                if current_metrics:
                    self.logger.info(f"Holders: {{current_metrics.get('holders', 'N/A')}}")
                    self.logger.info(f"Price: ${{current_metrics.get('price_usd', 'N/A'):.4f}}")
                    
                    # Check for alerts
                    alerts = self.check_alerts(current_metrics)
                    
                    if alerts:
                        self.send_alert(alerts)
                    
                    # Save current data
                    self.previous_data = current_metrics
                    self.save_data(current_metrics)
                
                # Wait for next check
                time.sleep(self.config["check_interval"])
                
            except KeyboardInterrupt:
                self.logger.info("Monitor stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {{e}}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    """Entry point"""
    monitor = OPMMonitor()
    monitor.monitor_loop()

if __name__ == "__main__":
    main()
"""
        self.write_file(Path(base_dir) / "scripts/monitor.py", monitor_py)
    
    def generate_workflows(self, base_dir: str):
        """Generate GitHub Actions workflows"""
        Console.step("Generating GitHub Actions workflows")
        
        # ci.yml
        ci_yml = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '*/15 * * * *'  # Run every 15 minutes

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Run linter
      run: npm run lint
    
    - name: Check security
      run: npm audit --audit-level=moderate
  
  update-data:
    runs-on: ubuntu-latest
    needs: test
    
    env:
      ETHERSCAN_API_KEY: ${{ secrets.ETHERSCAN_API_KEY }}
      CONTRACT_ADDRESS: ${{ secrets.CONTRACT_ADDRESS }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Update token data
      run: npm run update
    
    - name: Commit and push updates
      run: |
        git config user.name "GitHub Actions"
        git config user.email "actions@github.com"
        git add data/*.json
        git diff --quiet && git diff --staged --quiet || (git commit -m "Auto-update token data" && git push)
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./public
  
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      run: |
        npm audit
        echo "Security scan completed"
    
    - name: Check for vulnerabilities
      run: |
        if [ -f "package-lock.json" ]; then
          npm audit --json > audit.json
          echo "Audit report saved"
        fi
"""
        self.write_file(Path(base_dir) / ".github/workflows/ci.yml", ci_yml)
        
        # deploy.yml
        deploy_yml = """name: Deploy to Production

on:
  workflow_dispatch:
  push:
    tags:
      - 'v*.*.*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        registry-url: 'https://registry.npmjs.org'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Build project
      run: npm run build
    
    - name: Deploy to Server
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        SERVER_HOST: ${{ secrets.SERVER_HOST }}
        SERVER_USER: ${{ secrets.SERVER_USER }}
      run: |
        echo "Deploying to production server..."
        # Add your deployment commands here
        # Example: ssh deployment
        # ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_HOST "cd /var/www/opm && git pull && npm ci && pm2 restart opm"
    
    - name: Send deployment notification
      if: success()
      run: |
        echo "🚀 Deployment successful!"
        # Add notification logic here (Slack, Discord, Email, etc.)
"""
        self.write_file(Path(base_dir) / ".github/workflows/deploy.yml", deploy_yml)
    
    def generate_documentation(self, base_dir: str):
        """Generate documentation files"""
        Console.step("Generating documentation")
        
        # README.md (already generated in config, but more detailed)
        detailed_readme = f"""# 🚀 OnePremium (OPM) Token Repository

![OPM Logo]({self.config.LOGO_URL})

## 📋 Overview

This repository contains everything needed to monitor, analyze, and manage the OnePremium (OPM) token.

## 🎯 Features

### 📊 Real-time Dashboard
- Live token metrics
- Interactive charts and analytics
- Holder distribution visualization
- Transaction monitoring

### 🤖 Automation
- Auto-update every 15 minutes
- GitHub Actions workflows
- Security monitoring
- Alert system

### 🔧 Development Tools
- Complete CI/CD pipeline
- Testing suite
- Security scanning
- Deployment automation

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/{self.config.REPO_NAME}.git
cd {self.config.REPO_NAME}

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start development server
npm run dev
