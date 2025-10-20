# Selenium Tests - GitHub-Centric Workflow

A CI/CD-ready Selenium testing framework that works in GitHub Actions and Termux.

## 🚀 Features

- **GitHub Actions Integration** - Automated testing on push/PR/schedule
- **Multi-Environment Support** - Works in GitHub Actions, Termux, and local
- **CI/CD Pipeline** - Automated test reports and artifacts
- **Dual Testing Strategy** - Selenium + requests-based fallback

## 📊 GitHub Actions

The repository includes two workflows:

1. **Termux CI Tests** - Runs on every push/PR with matrix testing
2. **Selenium Integration Tests** - Manual/weekly comprehensive tests

## 🛠️ Local/Termux Usage

```bash
# Clone repository
git clone https://github.com/your-username/selenium_tests.git
cd selenium_tests

# Setup environment
./scripts/setup_termux.sh

# Run CI test suite
./scripts/run_ci_tests.sh

# Check Selenium availability
python scripts/selenium_ci.py --check-only

# Run specific tests
python -m pytest tests/test_network.py -v