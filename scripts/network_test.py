#!/usr/bin/env python3
"""
Network testing module for Termux - No browser required
"""

import os
import time
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class TermuxNetworkTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": "Termux",
            "tests": {}
        }
    
    def test_requests_scraping(self):
        """Test web scraping using requests + BeautifulSoup"""
        print("\n🕸️ Testing Requests-based Scraping...")
        
        test_urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json",
            "https://example.com"
        ]
        
        scraping_results = {}
        
        for url in test_urls:
            try:
                start_time = time.time()
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Termux) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=30)
                load_time = time.time() - start_time
                
                # Parse with BeautifulSoup for HTML
                if 'html' in url:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.title.string if soup.title else "No title"
                    scraping_results[url] = {
                        "status": "success",
                        "load_time": round(load_time, 2),
                        "status_code": response.status_code,
                        "title": title,
                        "content_length": len(response.content)
                    }
                else:
                    # For JSON responses
                    scraping_results[url] = {
                        "status": "success", 
                        "load_time": round(load_time, 2),
                        "status_code": response.status_code,
                        "content_type": response.headers.get('content-type', 'unknown')
                    }
                
                print(f"✅ {url}: {load_time:.2f}s")
                
            except Exception as e:
                scraping_results[url] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"❌ {url}: {e}")
        
        self.results["tests"]["web_scraping"] = scraping_results
        return scraping_results
    
    def test_network_speed(self):
        """Test network speed using speedtest-cli"""
        print("\n🚀 Testing Network Speed...")
        
        try:
            import speedtest
            
            st = speedtest.Speedtest()
            st.get_best_server()
            
            print("📡 Testing download speed...")
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            
            print("📡 Testing upload speed...")
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            ping = st.results.ping
            
            speed_results = {
                "download_mbps": round(download_speed, 2),
                "upload_mbps": round(upload_speed, 2),
                "ping_ms": round(ping, 2),
                "server": st.results.server['name'],
                "status": "success"
            }
            
            print(f"✅ Download: {download_speed:.2f} Mbps")
            print(f"✅ Upload: {upload_speed:.2f} Mbps") 
            print(f"✅ Ping: {ping:.2f} ms")
            
            self.results["tests"]["network_speed"] = speed_results
            return speed_results
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Speed test failed: {e}")
            self.results["tests"]["network_speed"] = error_result
            return error_result
    
    def test_latency(self):
        """Test latency to various websites"""
        print("\n📡 Testing Latency...")
        
        test_sites = [
            "https://www.google.com",
            "https://www.github.com",
            "https://httpbin.org"
        ]
        
        latency_results = {}
        
        for site in test_sites:
            try:
                times = []
                for i in range(3):  # Test 3 times for average
                    start_time = time.time()
                    response = requests.get(site, timeout=10)
                    end_time = time.time()
                    latency = (end_time - start_time) * 1000  # Convert to ms
                    times.append(latency)
                    time.sleep(1)  # Wait between tests
                
                avg_latency = sum(times) / len(times)
                latency_results[site] = {
                    "latency_ms": round(avg_latency, 2),
                    "status_code": response.status_code,
                    "status": "success"
                }
                print(f"✅ {site}: {avg_latency:.2f} ms")
                
            except Exception as e:
                latency_results[site] = {
                    "latency_ms": None,
                    "status": "error", 
                    "error": str(e)
                }
                print(f"❌ {site}: {e}")
        
        self.results["tests"]["latency"] = latency_results
        return latency_results
    
    def test_dns_resolution(self):
        """Test DNS resolution times"""
        print("\n🌐 Testing DNS Resolution...")
        
        domains = ["google.com", "github.com", "example.com"]
        dns_results = {}
        
        try:
            import socket
            
            for domain in domains:
                start_time = time.time()
                try:
                    ip = socket.gethostbyname(domain)
                    resolve_time = (time.time() - start_time) * 1000
                    
                    dns_results[domain] = {
                        "ip_address": ip,
                        "resolve_time_ms": round(resolve_time, 2),
                        "status": "success"
                    }
                    print(f"✅ {domain} → {ip}: {resolve_time:.2f} ms")
                    
                except Exception as e:
                    dns_results[domain] = {
                        "status": "error",
                        "error": str(e)
                    }
                    print(f"❌ {domain}: {e}")
                    
        except ImportError:
            dns_results = {"status": "skipped", "reason": "socket not available"}
            print("ℹ️ DNS test skipped")
        
        self.results["tests"]["dns_resolution"] = dns_results
        return dns_results
    
    def run_all_tests(self):
        """Run all network tests"""
        print("🎯 Starting Network Test Suite...")
        print("=" * 50)
        
        try:
            self.test_requests_scraping()
            time.sleep(2)
            
            self.test_network_speed() 
            time.sleep(2)
            
            self.test_latency()
            time.sleep(2)
            
            self.test_dns_resolution()
            
            # Save results
            self.save_results()
            
            print("\n" + "=" * 50)
            print("🎊 ALL NETWORK TESTS COMPLETED!")
            print("📊 Results saved to: network_test_results.json")
            
            return self.results
            
        except Exception as e:
            print(f"💥 Network test suite failed: {e}")
            return None
    
    def save_results(self):
        """Save results to JSON file"""
        filename = "network_test_results.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Also print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n📈 NETWORK TEST SUMMARY:")
        print("-" * 40)
        
        for test_name, test_result in self.results["tests"].items():
            if isinstance(test_result, dict) and 'status' in test_result:
                status = "✅ PASS" if test_result.get('status') == 'success' else "❌ FAIL"
                print(f"{test_name:20} {status}")
            else:
                # For nested results
                success_count = sum(1 for r in test_result.values() if r.get('status') == 'success')
                total_count = len(test_result)
                print(f"{test_name:20} {success_count}/{total_count} passed")

def main():
    """Main function"""
    print("🚀 Termux Network Test Runner")
    print("Using requests + speedtest (no browser required)")
    
    try:
        tester = TermuxNetworkTester()
        results = tester.run_all_tests()
        
        if results:
            print("\n🎉 All network tests completed successfully!")
            return 0
        else:
            print("\n💥 Some network tests failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Network tests interrupted by user")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())