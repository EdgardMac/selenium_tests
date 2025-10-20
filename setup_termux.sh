#!/data/data/com.termux/files/usr/bin/bash
echo "🔧 Termux Setup Script"
echo "======================"

# Create necessary directories
mkdir -p test_results

# Update and install system packages
echo "📦 Updating packages..."
pkg update -y && pkg upgrade -y

echo "📦 Installing system dependencies..."
pkg install -y python git wget

# Install Python requirements
echo "🐍 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements/requirements.txt

# Try to install Selenium components
echo "🚀 Attempting Selenium setup..."
if pkg install -y firefox geckodriver 2>/dev/null; then
    pip install -r requirements/requirements_selenium.txt
    echo "✅ Selenium components installed"
else
    echo "⚠️  Selenium not available, using requests-based tests only"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo "🎯 Run: ./run_ci_tests.sh"
echo "🔍 Or test individually:"
echo "   python scripts/selenium_ci.py --check-only"
echo "   python scripts/network_tests.py"