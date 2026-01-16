#!/usr/bin/env python3
"""
OPM Token Repository Auto-Creator
Run directly from iPhone/iSH with: python3 opm_deployer.py
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class OPMDeployer:
    def __init__(self):
        self.config = {
            # Hardcoded OPM specific values
            "contract_address": "0xE430b07F7B168E77b07b29482DbF89EafA53f484",
            "etherscan_api": "K7NFZ3QVDRHN2GGB9T8CB8IX3FNQA1928E",
            "logo_url": "https://onepremium.de/assets/opm-logo",
            "coinmarketcap_url": "https://dex.coinmarketcap.com/token/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484/",
            "uniswap_url": "https://app.uniswap.org/explore/tokens/ethereum/0xe430b07f7b168e77b07b29482dbf89eafa53f484",
            "etherscan_url": "https://etherscan.io/token/0xE430b07F7B168E77b07b29482DbF89EafA53f484",
            
            # GitHub Configuration (will be collected)
            "github_token": "",
            "repo_name": "onepremium-token",
            "description": "OnePremium (OPM) Token - Complete Dashboard & Automation",
            "is_private": False,
            "username": "",
            "email": ""
        }
        
        self.base_dir = Path.cwd()
        
    def run_command(self, cmd: str, check: bool = True) -> tuple:
        """Execute shell command with better error handling"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                check=check
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout.strip(), e.stderr.strip()
    
    def check_dependencies(self) -> bool:
        """Check for required dependencies"""
        dependencies = ["git", "curl"]
        missing = []
        
        print("🔍 Checking dependencies...")
        for dep in dependencies:
            code, _, _ = self.run_command(f"which {dep}", check=False)
            if code != 0:
                missing.append(dep)
        
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
            print("\nInstall missing dependencies:")
            if "git" in missing:
                print("  For iSH: apk add git")
            if "curl" in missing:
                print("  For iSH: apk add curl")
            return False
        
        print("✅ All dependencies found")
        return True
    
    def get_user_info(self):
        """Collect GitHub and user information"""
        print("\n" + "="*60)
        print("🚀 OnePremium (OPM) Token Repository Auto-Deployer")
        print("="*60 + "\n")
        
        print("📋 OPM Configuration (Auto-detected):")
        print(f"   Contract: {self.config['contract_address']}")
        print(f"   Etherscan API: {self.config['etherscan_api'][:8]}...")
        print(f"   Logo URL: {self.config['logo_url']}")
        
        print("\n🔑 GitHub Configuration:")
        
        # Get GitHub token
        while not self.config['github_token']:
            token = input("Enter GitHub Personal Access Token: ").strip()
            if token:
                self.config['github_token'] = token
            else:
                print("❌ Token is required!")
        
        # Get repo name
        repo = input(f"Repository name [{self.config['repo_name']}]: ").strip()
        if repo:
            self.config['repo_name'] = repo
        
        # Get description
        desc = input(f"Description: ").strip()
        if desc:
            self.config['description'] = desc
        
        # Get privacy
        private = input("Make private? (y/N): ").strip().lower()
        self.config['is_private'] = private == 'y'
        
        # Get user info
        self.config['username'] = input("GitHub Username: ").strip()
        self.config['email'] = input("Email Address: ").strip()
        
        # Save config for future use
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        config_path = self.base_dir / "opm_config.json"
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✅ Configuration saved to {config_path}")
    
    def create_github_repo(self) -> bool:
        """Create GitHub repository using API"""
        print("\n🌐 Creating GitHub repository...")
        
        headers = {
            "Authorization": f"token {self.config['github_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "name": self.config['repo_name'],
            "description": self.config['description'],
            "private": self.config['is_private'],
            "auto_init": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }
        
        try:
            response = requests.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                repo_data = response.json()
                self.config['repo_url'] = repo_data['html_url']
                self.config['clone_url'] = repo_data['clone_url']
                print(f"✅ Repository created: {self.config['repo_url']}")
                return True
            else:
                print(f"❌ Failed to create repository: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating repository: {e}")
            return False
    
    def setup_git(self):
        """Configure git user"""
        print("\n⚙️ Setting up git configuration...")
        
        self.run_command(f'git config --global user.name "{self.config["username"]}"')
        self.run_command(f'git config --global user.email "{self.config["email"]}"')
        
        print("✅ Git configured")
    
    def create_project_structure(self):
        """Create all files and directories"""
        print("\n📁 Creating project structure...")
        
        # Create directories
        directories = [
            "scripts",
            "public",
            "contracts",
            "dao",
            "docs",
            ".github/workflows",
            "test"
        ]
        
        for directory in directories:
            dir_path = self.base_dir / self.config['repo_name'] / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  📂 {directory}")
        
        # Create all files
        self.create_files()
        
        print("✅ Project structure created")
    
    def create_files(self):
        """Create all project files"""
        files = {
            # Root files
            'README.md': self.create_readme(),
            'whitepaper.md': self.create_whitepaper(),
            'LICENSE': self.create_license(),
            'package.json': self.create_package_json(),
            '.gitignore': self.create_gitignore(),
            '.env.example': self.create_env_example(),
            
            # Config
            'config.json': self.create_config_json(),
            
            # Main scripts
            'scripts/update_data.py': self.create_update_script(),
            'scripts/deploy_github.py': self.create_deploy_script(),
            'scripts/monitor.py': self.create_monitor_script(),
            
            # Node.js scripts (compatibility)
            'scripts/update.js': self.create_js_update_script(),
            'scripts/config.js': self.create_js_config(),
            
            # Public files
            'public/index.html': self.create_index_html(),
            'public/dashboard.html': self.create_dashboard_html(),
            'public/style.css': self.create_css(),
            'public/app.js': self.create_app_js(),
            'public/opm-logo.svg': self.fetch_logo(),
            
            # GitHub Actions
            '.github/workflows/update.yml': self.create_github_action(),
            '.github/workflows/deploy.yml': self.create_deploy_action(),
            '.github/dependabot.yml': self.create_dependabot(),
            
            # Documentation
            'docs/API.md': self.create_api_docs(),
            'docs/SETUP.md': self.create_setup_guide(),
            
            # Smart Contracts (placeholder)
            'contracts/OPM.sol': self.create_opm_contract(),
            
            # Quick setup script
            'setup.sh': self.create_setup_script(),
            
            # Mobile-friendly runner
            'run_mobile.py': self.create_mobile_runner()
        }
        
        for filepath, content in files.items():
            full_path = self.base_dir / self.config['repo_name'] / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if content:
                with open(full_path, 'w') as f:
                    f.write(content)
                print(f"  📄 {filepath}")
        
        # Make scripts executable
        scripts = ['scripts/update_data.py', 'scripts/monitor.py', 'setup.sh']
        for script in scripts:
            script_path = self.base_dir / self.config['repo_name'] / script
            script_path.chmod(0o755)
    
    def create_readme(self) -> str:
        return f"""# OnePremium (OPM) Token Repository

![OPM Logo]({self.config['logo_url']})

{self.config['description']}

## 🎯 Quick Deployment

```bash
# Clone and setup
git clone https://github.com/{self.config['username']}/{self.config['repo_name']}.git
cd {self.config['repo_name']}
chmod +x setup.sh
./setup.sh