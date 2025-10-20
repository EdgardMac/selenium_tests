import pytest
import requests
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
    
    @pytest.mark.slow  
    def test_network_speed(self, network_tester):
        """Test network speed measurement"""
        result = network_tester.test_network_speed()
        assert isinstance(result, dict)