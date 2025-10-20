#!/usr/bin/env python3
"""
Main test runner for Selenium Termux Tests
"""

import os
import sys

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

def main():
    print("🎯 Selenium Termux Test Suite")
    print("=" * 40)
    
    # Check if running in Termux
    if not os.path.exists('/data/data/com.termux/files/home'):
        print("⚠️  Warning: Not running in Termux environment")
        print("Some features might not work correctly")
    
    try:
        from scripts.selenium_test import TermuxSeleniumTester
        
        # Run the tests
        tester = TermuxSeleniumTester(headless=True)
        results = tester.run_all_tests()
        
        if results:
            print("\n🎉 All tests completed!")
            return 0
        else:
            print("\n💥 Tests failed!")
            return 1
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())