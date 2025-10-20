#!/bin/bash
echo "🎯 Running GitHub CI Test Suite"
echo "================================"

# Run network tests (always available)
echo "🌐 Running network tests..."
python -m pytest tests/test_network.py -v

# Try Selenium tests if available
if python scripts/selenium_ci.py --check-only; then
    echo "🚀 Running Selenium tests..."
    python scripts/selenium_ci.py
    python -m pytest tests/test_selenium.py -v -m "slow"
else
    echo "⚠️  Skipping Selenium tests (not available)"
fi

# Generate combined report
echo "📊 Generating test report..."
if [ -f "ci_test_results.json" ]; then
    python -c "
import json
try:
    with open('ci_test_results.json') as f:
        data = json.load(f)
    print('Test Environment:', data.get('environment', 'unknown'))
    print('Tests Run:', len(data.get('tests', {})))
    print('Successful:', sum(1 for t in data['tests'].values() if t.get('status') == 'success'))
except Exception as e:
    print('Error generating report:', e)
"
fi

echo "✅ CI test suite completed!"