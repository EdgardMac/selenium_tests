import pytest
import os
from scripts.selenium_ci import GitHubSeleniumRunner

class TestSeleniumCI:
    @pytest.fixture
    def selenium_runner(self):
        return GitHubSeleniumRunner(headless=True)
    
    def test_environment_detection(self, selenium_runner):
        """Test environment detection"""
        env = selenium_runner.detect_environment()
        assert env in ['github_actions', 'termux', 'local']
    
    def test_geckodriver_discovery(self, selenium_runner):
        """Test geckodriver path discovery"""
        path = selenium_runner.find_geckodriver()
        assert isinstance(path, str)
    
    @pytest.mark.slow
    def test_selenium_setup(self, selenium_runner):
        """Test Selenium driver setup"""
        driver = selenium_runner.setup_selenium()
        if driver:
            driver.quit()
            assert True
        else:
            pytest.skip("Selenium not available in this environment")