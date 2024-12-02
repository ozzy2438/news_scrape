import yaml
import os
from selenium.webdriver.chrome.service import Service

class Config:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.setup_chromedriver()

    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            config_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(config_dir, os.path.basename(config_path))
            
            with open(full_path, 'r') as file:
                config = yaml.safe_load(file)
                
            self.headless = config.get('headless', False)
            self.timeout = config.get('timeout', 15)
            self.output_dir = os.path.abspath(config.get('output_dir', 'output'))
            
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    def setup_chromedriver(self):
        """Setup ChromeDriver using system installation"""
        try:
            self.chromedriver_path = "/opt/homebrew/bin/chromedriver"
            self.service = Service(self.chromedriver_path)
        except Exception as e:
            raise Exception(f"Error setting up ChromeDriver: {str(e)}")

    def get_service(self):
        """Get ChromeDriver service"""
        return self.service