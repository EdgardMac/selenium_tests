import pytest
import requests
import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.network_tests import TermuxNetworkTester

class TestNetwork:
    @pytest.fixture
    def network_tester(self):
        return TermuxNetworkTester()
    
    def test_requests_available(self):
        """Test that requests module is available"""
        import requests
        assert requests.__version__ is not None
    
    def test_httpbin_connectivity(self):
        """Test connectivity to httpbin"""
        response = requests.get("https://httpbin.org/json", timeout=10)
        assert response.status_code == 200
    
    def test_network_tester_initialization(self, network_tester):
        """Test that network tester initializes correctly"""
        assert network_tester is not None
        assert 'timestamp' in network_tester.results
        assert network_tester.results['environment'] == 'Termux'
    
    @pytest.mark.slow  
    def test_network_speed_measurement(self, network_tester):
        """Test network speed measurement functionality"""
        result = network_tester.test_network_speed()
        assert isinstance(result, dict)
    
    def test_latency_measurement(self, network_tester):
        """Test latency measurement functionality"""
        result = network_tester.test_latency()
        assert isinstance(result, dict)
    
    def test_dns_resolution(self, network_tester):
        """Test DNS resolution functionality"""
        result = network_tester.test_dns_resolution()
        assert isinstance(result, dict)