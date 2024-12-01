import yaml
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class Config:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.setup_chromedriver()

    def load_config(self, config_path):
        [Rest of config.py content...]