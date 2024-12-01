import unittest
from unittest.mock import MagicMock, patch
from scraper import WebScraper
import os

class TestWebScraper(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.scraper = WebScraper()
        
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'scraper'):
            if hasattr(self.scraper, 'driver'):
                self.scraper.driver.quit()
                
    @patch('selenium.webdriver.Chrome')
    def test_setup_driver(self, mock_chrome):
        """Test WebDriver initialization"""
        self.scraper.setup_driver()
        self.assertTrue(mock_chrome.called)
        
    def test_extract_data(self):
        """Test data extraction"""
        # Mock the WebDriver
        self.scraper.driver = MagicMock()
        self.scraper.wait = MagicMock()
        
        # Mock element
        mock_element = MagicMock()
        mock_element.text = "Test Data"
        self.scraper.wait.until.return_value = mock_element
        
        # Test extraction
        selectors = {"test_field": "div.test"}
        data = self.scraper.extract_data(selectors)
        
        self.assertEqual(data["test_field"], "Test Data")
        
    def test_save_to_csv(self):
        """Test CSV file creation"""
        test_data = {"field1": ["value1"], "field2": ["value2"]}
        test_filename = "test_output"
        
        self.scraper.save_to_csv(test_data, test_filename)
        
        # Check if file exists
        self.assertTrue(os.path.exists(f"output/{test_filename}.csv"))
        
        # Clean up
        os.remove(f"output/{test_filename}.csv")

if __name__ == '__main__':
    unittest.main()