#!/usr/bin/env python3
"""
Selenium Web Scraping Test for Termux
Uses Firefox with GeckoDriver (works better in Termux)
"""

import os
import sys
import time
import json
from datetime import datetime
from urllib.parse import urlparse

try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
except ImportError as e:
    print(f"❌ Selenium not installed: {e}")
    print("Run: pip install selenium")
    sys.exit(1)


class TermuxSeleniumTester:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {}
        }
        
    def setup_driver(self):
        """Setup Firefox driver for Termux"""
        print("🚀 Setting up Firefox driver...")
        
        try:
            # Firefox options for Termux
            options = Options()
            
            if self.headless:
                options.add_argument("--headless")
            
            # Options that work better in Termux environment
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # Set user agent
            options.set_preference("general.useragent.override", 
                                 "Mozilla/5.0 (Linux; Android 10; Termux) AppleWebKit/537.36")
            
            # Setup service
            service = Service(
                executable_path=os.path.join(os.path.expanduser("~"), "geckodriver"),
                log_path=os.path.devnull  # Disable logs for cleaner output
            )
            
            # Create driver
            self.driver = webdriver.Firefox(service=service, options=options)
            print("✅ Firefox driver started successfully!")
            
        except Exception as e:
            print(f"❌ Failed to start driver: {e}")
            raise
    
    def test_google_search(self):
        """Test Google search functionality"""
        print("\n🔍 Testing Google Search...")
        
        try:
            self.driver.get("https://www.google.com")
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, 10)
            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Perform search
            search_term = "Termux Selenium Test"
            search_box.send_keys(search_term)
            search_box.submit()
            
            # Wait for results
            wait.until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Get results
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
            result_count = len(results)
            
            test_result = {
                "status": "success",
                "search_term": search_term,
                "results_found": result_count,
                "page_title": self.driver.title,
                "url": self.driver.current_url
            }
            
            print(f"✅ Google search successful! Found {result_count} results")
            self.results["tests"]["google_search"] = test_result
            return test_result
            
        except Exception as e:
            error_msg = f"Google search failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["tests"]["google_search"] = {
                "status": "error",
                "error": error_msg
            }
            return None
    
    def test_web_scraping(self, url="https://httpbin.org/html"):
        """Test basic web scraping"""
        print(f"\n🕸️ Testing web scraping: {url}")
        
        try:
            self.driver.get(url)
            
            # Wait for page load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract page information
            page_info = {
                "title": self.driver.title,
                "url": self.driver.current_url,
                "content_length": len(self.driver.page_source),
                "headers": list(self.driver.get_cookies())[:3]  # First 3 cookies
            }
            
            # Try to extract some text content
            try:
                paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
                page_info["paragraph_count"] = len(paragraphs)
                
                if paragraphs:
                    page_info["sample_text"] = paragraphs[0].text[:100] + "..." if len(paragraphs[0].text) > 100 else paragraphs[0].text
            except:
                page_info["paragraph_count"] = 0
            
            test_result = {
                "status": "success",
                "page_info": page_info
            }
            
            print(f"✅ Web scraping successful! Title: '{self.driver.title}'")
            self.results["tests"]["web_scraping"] = test_result
            return test_result
            
        except Exception as e:
            error_msg = f"Web scraping failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["tests"]["web_scraping"] = {
                "status": "error", 
                "error": error_msg
            }
            return None
    
    def test_network_speed(self):
        """Test page load speed"""
        print("\n⚡ Testing page load speed...")
        
        test_urls = [
            "https://www.google.com",
            "https://httpbin.org/html", 
            "https://example.com"
        ]
        
        speed_results = {}
        
        for url in test_urls:
            try:
                start_time = time.time()
                self.driver.get(url)
                
                # Wait for page to be interactive
                WebDriverWait(self.driver, 15).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                load_time = time.time() - start_time
                speed_results[url] = {
                    "load_time_seconds": round(load_time, 2),
                    "status": "success"
                }
                
                print(f"✅ {url}: {load_time:.2f}s")
                
            except Exception as e:
                speed_results[url] = {
                    "load_time_seconds": None,
                    "status": "error",
                    "error": str(e)
                }
                print(f"❌ {url}: Failed - {e}")
        
        self.results["tests"]["network_speed"] = speed_results
        return speed_results
    
    def run_all_tests(self):
        """Run all selenium tests"""
        print("🎯 Starting Selenium Test Suite...")
        print("=" * 50)
        
        try:
            self.setup_driver()
            
            # Run tests
            self.test_google_search()
            time.sleep(2)  # Brief pause between tests
            
            self.test_web_scraping()
            time.sleep(2)
            
            self.test_network_speed()
            
            # Save results
            self.save_results()
            
            print("\n" + "=" * 50)
            print("🎊 ALL TESTS COMPLETED!")
            print(f"📊 Results saved to: {os.path.abspath('selenium_results.json')}")
            
            return self.results
            
        except Exception as e:
            print(f"💥 Test suite failed: {e}")
            return None
        finally:
            self.cleanup()
    
    def save_results(self):
        """Save test results to JSON file"""
        filename = "selenium_results.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            print("\n🧹 Cleaning up...")
            try:
                self.driver.quit()
                print("✅ Driver closed successfully")
            except:
                print("⚠️  Error closing driver")


def main():
    """Main function to run the tests"""
    print("🚀 Selenium Termux Test Runner")
    print("This may take a few minutes...")
    
    try:
        tester = TermuxSeleniumTester(headless=True)
        results = tester.run_all_tests()
        
        if results:
            # Print summary
            print("\n📈 TEST SUMMARY:")
            print("-" * 30)
            for test_name, test_result in results["tests"].items():
                status = "✅ PASS" if test_result.get("status") == "success" else "❌ FAIL"
                print(f"{test_name}: {status}")
            
            print(f"\n📁 Results saved to: selenium_results.json")
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")


if __name__ == "__main__":
    main()