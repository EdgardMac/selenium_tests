#!/usr/bin/env python3
"""
Selenium CI Test Runner for GitHub Actions and Termux
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime

class GitHubSeleniumRunner:
    def __init__(self, headless=True):
        self.headless = headless
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self.detect_environment(),
            "runner": "GitHub Actions" if self.is_github_actions() else "Termux",
            "tests": {}
        }
    
    def detect_environment(self):
        """Detect if running in GitHub Actions or Termux"""
        if self.is_github_actions():
            return "github_actions"
        elif self.is_termux():
            return "termux"
        else:
            return "local"
    
    def is_github_actions(self):
        return os.getenv('GITHUB_ACTIONS') == 'true'
    
    def is_termux(self):
        return os.path.exists('/data/data/com.termux/files/home')
    
    def setup_selenium(self):
        """Setup Selenium based on environment"""
        print(f"🔧 Setting up Selenium for {self.results['environment']}...")
        
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service
            
            options = Options()
            
            if self.headless or self.is_github_actions():
                options.add_argument("--headless")
            
            # Common options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # Environment-specific configurations
            if self.is_github_actions():
                # GitHub Actions - use system geckodriver
                service = Service('/usr/bin/geckodriver')
            else:
                # Termux or local - try to find geckodriver
                geckodriver_path = self.find_geckodriver()
                service = Service(executable_path=geckodriver_path)
            
            driver = webdriver.Firefox(service=service, options=options)
            print("✅ Selenium driver initialized successfully")
            return driver
            
        except Exception as e:
            print(f"❌ Selenium setup failed: {e}")
            return None
    
    def find_geckodriver(self):
        """Find geckodriver in common locations"""
        possible_paths = [
            '/usr/bin/geckodriver',
            '/usr/local/bin/geckodriver',
            os.path.expanduser('~/geckodriver'),
            os.path.join(os.getcwd(), 'geckodriver')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try which command
        import subprocess
        try:
            result = subprocess.run(['which', 'geckodriver'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return 'geckodriver'  # Hope it's in PATH
    
    def run_ci_tests(self):
        """Run CI-optimized tests"""
        print("🎯 Running CI Selenium Tests...")
        
        driver = self.setup_selenium()
        if not driver:
            return self.results
        
        try:
            # Test 1: Basic navigation
            self.test_basic_navigation(driver)
            
            # Test 2: Form interaction
            self.test_form_interaction(driver)
            
            # Test 3: JavaScript execution
            self.test_javascript(driver)
            
            # Test 4: Screenshot capability
            if not self.is_github_actions():
                self.test_screenshot(driver)
            
        finally:
            driver.quit()
        
        self.save_results()
        return self.results
    
    def test_basic_navigation(self, driver):
        """Test basic web navigation"""
        print("🌐 Testing basic navigation...")
        
        try:
            test_url = "https://httpbin.org/html"
            driver.get(test_url)
            
            title = driver.title
            current_url = driver.current_url
            
            self.results["tests"]["basic_navigation"] = {
                "status": "success",
                "title": title,
                "url": current_url,
                "environment": self.results["environment"]
            }
            print(f"✅ Basic navigation: {title}")
            
        except Exception as e:
            self.results["tests"]["basic_navigation"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Basic navigation failed: {e}")
    
    def test_form_interaction(self, driver):
        """Test form interaction capabilities"""
        print("📝 Testing form interaction...")
        
        try:
            driver.get("https://httpbin.org/forms/post")
            
            # Find and interact with form elements
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            wait = WebDriverWait(driver, 10)
            input_field = wait.until(
                EC.presence_of_element_located((By.NAME, "custname"))
            )
            
            input_field.send_keys("CI Test User")
            entered_text = input_field.get_attribute("value")
            
            self.results["tests"]["form_interaction"] = {
                "status": "success",
                "entered_text": entered_text,
                "environment": self.results["environment"]
            }
            print(f"✅ Form interaction: Entered '{entered_text}'")
            
        except Exception as e:
            self.results["tests"]["form_interaction"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Form interaction failed: {e}")
    
    def test_javascript(self, driver):
        """Test JavaScript execution"""
        print("⚡ Testing JavaScript execution...")
        
        try:
            result = driver.execute_script("return navigator.userAgent;")
            window_size = driver.execute_script(
                "return {width: window.innerWidth, height: window.innerHeight};"
            )
            
            self.results["tests"]["javascript"] = {
                "status": "success",
                "user_agent": result,
                "window_size": window_size,
                "environment": self.results["environment"]
            }
            print(f"✅ JavaScript execution: {result[:50]}...")
            
        except Exception as e:
            self.results["tests"]["javascript"] = {
                "status": "error", 
                "error": str(e)
            }
            print(f"❌ JavaScript execution failed: {e}")
    
    def test_screenshot(self, driver):
        """Test screenshot capability (skip in GitHub Actions)"""
        if self.is_github_actions():
            return
            
        print("📸 Testing screenshot...")
        
        try:
            screenshot_path = "ci_screenshot.png"
            driver.save_screenshot(screenshot_path)
            
            self.results["tests"]["screenshot"] = {
                "status": "success",
                "file": screenshot_path,
                "environment": self.results["environment"]
            }
            print(f"✅ Screenshot saved: {screenshot_path}")
            
        except Exception as e:
            self.results["tests"]["screenshot"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Screenshot failed: {e}")
    
    def save_results(self):
        """Save test results"""
        filename = "ci_test_results.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n📈 CI TEST SUMMARY:")
        print("=" * 50)
        for test_name, result in self.results["tests"].items():
            status = "✅ PASS" if result.get("status") == "success" else "❌ FAIL"
            print(f"{test_name:20} {status}")
        
        print(f"\n🏁 Environment: {self.results['environment']}")
        print(f"📊 Results saved to: ci_test_results.json")

def main():
    parser = argparse.ArgumentParser(description='Selenium CI Runner')
    parser.add_argument('--check-only', action='store_true', 
                       help='Only check Selenium availability')
    parser.add_argument('--comprehensive', action='store_true',
                       help='Run comprehensive tests')
    
    args = parser.parse_args()
    
    runner = GitHubSeleniumRunner(headless=True)
    
    if args.check_only:
        driver = runner.setup_selenium()
        if driver:
            print("✅ Selenium is available and working")
            driver.quit()
            return 0
        else:
            print("❌ Selenium is not available")
            return 1
    else:
        results = runner.run_ci_tests()
        success_count = sum(1 for r in results["tests"].values() 
                          if r.get("status") == "success")
        return 0 if success_count > 0 else 1

if __name__ == "__main__":
    sys.exit(main())