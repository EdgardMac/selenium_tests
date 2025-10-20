#!/usr/bin/env python3
"""
Fixed test runner for Termux - No browser required
"""

import os
import sys

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['requests', 'beautifulsoup4', 'speedtest-cli']
    missing = []
    
    for package in required_packages:
        try:
            if package == 'speedtest-cli':
                import speedtest
            elif package == 'beautifulsoup4':
                from bs4 import BeautifulSoup
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    print("🎯 Termux Network Test Suite")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Please install with: pip install " + " ".join(missing))
        return 1
    
    try:
        from scripts.selenium_test_fixed import TermuxNetworkTester
        
        tester = TermuxNetworkTester()
        results = tester.run_all_tests()
        
        if results:
            print("\n✅ Test suite completed!")
            print("📁 Results saved to: network_test_results.json")
            return 0
        else:
            print("\n❌ Test suite failed!")
            return 1
            
    except Exception as e:
        print(f"💥 Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())