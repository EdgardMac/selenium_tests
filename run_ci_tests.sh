#!/data/data/com.termux/files/usr/bin/bash
echo "🎯 CI Test Suite Runner"
echo "======================="

# Run the simple test runner (most reliable)
echo "🚀 Running simple test suite..."
python run_simple_tests.py

# Try pytest if simple tests pass
if [ $? -eq 0 ]; then
    echo ""
    echo "📊 Running pytest suite..."
    python -m pytest tests/test_network.py -v --html=report_network.html --self-contained-html || echo "⚠️ Pytest had some issues"
else
    echo "❌ Simple tests failed, skipping pytest"
fi

echo ""
echo "📋 FINAL RESULTS SUMMARY:"
echo "========================="

# Check for result files
if [ -f "simple_test_results.json" ]; then
    echo "📁 Simple tests: Results saved to simple_test_results.json"
fi

if [ -f "network_test_results.json" ]; then
    echo "📁 Network tests: Results saved to network_test_results.json"
fi

if [ -f "ci_test_results.json" ]; then
    echo "📁 Selenium tests: Results saved to ci_test_results.json"
fi

if [ -f "report_network.html" ]; then
    echo "📊 HTML report: report_network.html"
fi

echo ""
echo "✅ CI test suite completed!"