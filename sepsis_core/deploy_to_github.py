#!/usr/bin/env python3
"""
ICU Sepsis Prediction System - GitHub Deployment Script

This script helps you deploy the complete project to your GitHub repository.
Run this script after downloading the project files.

Usage:
    python deploy_to_github.py

Requirements:
    - Git installed on your system
    - GitHub repository already created: icu-sepsis-prediction-system
    - Your GitHub personal access token set in environment or entered when prompted
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}..." if description else f"🔄 Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ Success: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def check_git_installed():
    """Check if Git is installed."""
    return run_command("git --version", "Checking Git installation")

def initialize_repo():
    """Initialize Git repository and set up remote."""
    commands = [
        ("git init", "Initializing Git repository"),
        ("git config user.email 'user@example.com'", "Setting Git email"),
        ("git config user.name 'ICU Sepsis System'", "Setting Git username"),
        ("git remote add origin https://github.com/arpitsawant11/icu-sepsis-prediction-system.git", "Adding GitHub remote")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_requirements_file():
    """Create requirements.txt file."""
    requirements = """streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
tensorflow>=2.13.0
scikit-learn>=1.3.0
joblib>=1.3.0"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✅ Created requirements.txt")

def create_dockerfile():
    """Create Dockerfile for containerized deployment."""
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create streamlit config directory
RUN mkdir -p ~/.streamlit

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:5000/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Created Dockerfile")

def create_github_workflow():
    """Create GitHub Actions workflow for CI/CD."""
    os.makedirs(".github/workflows", exist_ok=True)
    
    workflow_content = """name: ICU Sepsis Prediction CI/CD

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run basic import tests
      run: |
        python -c "import streamlit; import pandas; import numpy; import plotly"
        python -c "from models.sepsis_model import SepsisPredictor"
        python -c "from utils.data_processing import validate_patient_data"
        echo "✅ All imports successful"
    
    - name: Check Streamlit app syntax
      run: |
        python -m py_compile app.py
        echo "✅ Main app syntax is valid"
"""
    
    with open(".github/workflows/ci.yml", "w") as f:
        f.write(workflow_content)
    print("✅ Created GitHub Actions workflow")

def add_and_commit():
    """Add files and create initial commit."""
    commands = [
        ("git add .", "Adding all files to staging"),
        ("git commit -m 'Initial commit: ICU Sepsis Risk Prediction System\n\n- Deep learning model for sepsis risk assessment\n- Real-time patient monitoring dashboard\n- Clinical alert system with intervention recommendations\n- Comprehensive documentation and deployment configs'", "Creating initial commit")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def push_to_github():
    """Push to GitHub repository."""
    print("🚀 Pushing to GitHub...")
    print("Note: You may be prompted for your GitHub username and password/token")
    return run_command("git push -u origin main", "Pushing to GitHub")

def display_file_structure():
    """Display the project file structure."""
    print("\n📁 Project File Structure:")
    print("icu-sepsis-prediction-system/")
    print("├── README.md                 # Project documentation")
    print("├── requirements.txt          # Python dependencies")
    print("├── Dockerfile               # Docker configuration")
    print("├── .gitignore               # Git ignore rules")
    print("├── app.py                   # Main Streamlit application")
    print("├── components/              # UI components")
    print("│   ├── alerts.py           # Alert system")
    print("│   ├── dashboard.py        # Patient dashboard")
    print("│   └── patient_input.py    # Data input forms")
    print("├── models/")
    print("│   └── sepsis_model.py     # ML model implementation")
    print("├── utils/")
    print("│   ├── data_processing.py  # Data validation")
    print("│   └── risk_calculator.py  # Risk assessment")
    print("├── .streamlit/")
    print("│   └── config.toml         # Streamlit configuration")
    print("└── .github/")
    print("    └── workflows/")
    print("        └── ci.yml          # GitHub Actions CI/CD")

def main():
    """Main deployment function."""
    print("🏥 ICU Sepsis Prediction System - GitHub Deployment")
    print("=" * 55)
    
    # Check prerequisites
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first.")
        sys.exit(1)
    
    # Create additional files
    create_requirements_file()
    create_dockerfile()
    create_github_workflow()
    
    # Git operations
    if not initialize_repo():
        print("❌ Failed to initialize repository")
        sys.exit(1)
    
    if not add_and_commit():
        print("❌ Failed to create initial commit")
        sys.exit(1)
    
    # Push to GitHub
    if push_to_github():
        print("\n🎉 SUCCESS! Your ICU Sepsis Prediction System is now on GitHub!")
        print("🔗 Repository: https://github.com/arpitsawant11/icu-sepsis-prediction-system")
        print("\n📋 Next Steps:")
        print("1. Visit your GitHub repository to see the code")
        print("2. Deploy to Streamlit Cloud by connecting your GitHub repo")
        print("3. Or deploy using Docker with: docker build -t sepsis-app .")
        print("\n✨ Your medical AI system is ready to help save lives!")
    else:
        print("❌ Failed to push to GitHub. Please check your credentials and try again.")
        print("💡 You can manually push later with: git push -u origin main")
    
    display_file_structure()

if __name__ == "__main__":
    main()