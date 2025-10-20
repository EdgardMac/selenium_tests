#!/bin/bash
echo "🔧 Setting up Selenium in Termux..."

# Update packages
pkg update && pkg upgrade -y

# Install required system packages
pkg install -y python rust openjdk-17 wget

# Install Python packages
pip install --upgrade pip
pip install selenium==4.15.0 requests beautifulsoup4

# Install Chrome and ChromeDriver for Termux
echo "📥 Installing Chrome WebView..."
pkg install -y x11-repo
pkg install -y chromium

# Alternative: Use geckodriver (Firefox) which works better in Termux
echo "📥 Setting up GeckoDriver (Firefox)..."
wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux-aarch64.tar.gz
tar -xzf geckodriver-v0.34.0-linux-aarch64.tar.gz
chmod +x geckodriver
mv geckodriver $PREFIX/bin/

# Create test directory
mkdir -p ~/selenium-tests
cd ~/selenium-tests

echo "✅ Setup complete!"
echo "🚀 Run: python run_tests.py"