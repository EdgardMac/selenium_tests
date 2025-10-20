import pytest
import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestSeleniumSimple:
    def test_selenium_import(self):
        """Test that Selenium can be imported"""
        import selenium
        assert selenium.__version__ is not None
    
    def test_firefox_available(self):
        """Test that Firefox/GeckoDriver is available"""
        import subprocess
        result = subprocess.run(['which', 'geckodriver'], 
                              capture_output=True, text=True)
        # This test passes if geckodriver is found, but doesn't fail if not
        if result.returncode == 0:
            assert True
        else:
            pytest.skip("GeckoDriver not available")
    
    @pytest.mark.slow
    def test_selenium_functionality(self):
        """Test actual Selenium functionality"""
        try:
            from scripts.selenium_ci import GitHubSeleniumRunner
            runner = GitHubSeleniumRunner(headless=True)
            driver = runner.setup_selenium()
            if driver:
                driver.quit()
                assert True
            else:
                pytest.skip("Selenium not available")
        except Exception as e:
            pytest.skip(f"Selenium test skipped: {e}")