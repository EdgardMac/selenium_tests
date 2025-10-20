#!/bin/bash
echo "🔧 GitHub-Centric Termux Setup"
echo "==============================="

# Create results directory
mkdir -p test_results

# Install base packages
pkg update -y && pkg upgrade -y
pkg install -y python git wget

# Install Python requirements
pip install -r requirements/requirements.txt

# Try to install Selenium components
echo "🐍 Attempting Selenium setup..."
if pkg install -y firefox geckodriver 2>/dev/null; then
    pip install -r requirements/requirements_selenium.txt
    echo "✅ Selenium components installed"
else
    echo "⚠️  Selenium not available, using requests-based tests only"
fi

echo "🚀 Setup complete!"
echo "📁 Run: python scripts/selenium_ci.py --check-only"