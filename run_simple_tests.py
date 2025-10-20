#!/usr/bin/env python3
"""
Simple test runner that doesn't rely on pytest - Most reliable for Termux
"""
import sys
import os
import json
from datetime import datetime

# Add scripts to path
sys.path.insert(0, 'scripts')

def run_simple_tests():
    print("🎯 Simple Test Runner")
    print("====================")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "environment": "termux",
        "tests": {}
    }
    
    # Test 1: Import network_tests
    try:
        from network_tests import TermuxNetworkTester
        results["tests"]["import_network_tests"] = {"status": "success"}
        print("✅ Import network_tests: PASS")
    except Exception as e:
        results["tests"]["import_network_tests"] = {"status": "error", "error": str(e)}
        print(f"❌ Import network_tests: FAIL - {e}")
    
    # Test 2: Create network tester instance
    try:
        tester = TermuxNetworkTester()
        results["tests"]["create_tester"] = {"status": "success"}
        print("✅ Create tester instance: PASS")
    except Exception as e:
        results["tests"]["create_tester"] = {"status": "error", "error": str(e)}
        print(f"❌ Create tester instance: FAIL - {e}")
    
    # Test 3: Test requests
    try:
        import requests
        response = requests.get("https://httpbin.org/json", timeout=10)
        results["tests"]["requests_test"] = {"status": "success", "status_code": response.status_code}
        print(f"✅ Requests test: PASS (Status: {response.status_code})")
    except Exception as e:
        results["tests"]["requests_test"] = {"status": "error", "error": str(e)}
        print(f"❌ Requests test: FAIL - {e}")
    
    # Test 4: Test Selenium
    try:
        from selenium_ci import GitHubSeleniumRunner
        runner = GitHubSeleniumRunner(headless=True)
        driver = runner.setup_selenium()
        if driver:
            driver.quit()
            results["tests"]["selenium_test"] = {"status": "success"}
            print("✅ Selenium test: PASS")
        else:
            results["tests"]["selenium_test"] = {"status": "error", "error": "Driver not created"}
            print("❌ Selenium test: FAIL - Driver not created")
    except Exception as e:
        results["tests"]["selenium_test"] = {"status": "error", "error": str(e)}
        print(f"❌ Selenium test: FAIL - {e}")
    
    # Test 5: Run a quick network test
    try:
        tester = TermuxNetworkTester()
        latency_result = tester.test_latency()
        results["tests"]["network_latency"] = {"status": "success", "result": latency_result}
        print("✅ Network latency test: PASS")
    except Exception as e:
        results["tests"]["network_latency"] = {"status": "error", "error": str(e)}
        print(f"❌ Network latency test: FAIL - {e}")
    
    # Save results
    with open("simple_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n📊 SIMPLE TEST SUMMARY:")
    print("=" * 40)
    success_count = sum(1 for r in results["tests"].values() if r.get("status") == "success")
    total_count = len(results["tests"])
    
    for test_name, result in results["tests"].items():
        status = result.get("status", "unknown")
        icon = "✅" if status == "success" else "❌"
        print(f"{test_name:25} {icon} {status}")
    
    print(f"\n🏁 RESULTS: {success_count}/{total_count} tests passed")
    print("📁 Detailed results saved to: simple_test_results.json")
    
    return success_count == total_count

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)