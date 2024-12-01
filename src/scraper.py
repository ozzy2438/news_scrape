from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import logging
import os
import sys
import time
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config

class WebScraper:
    def __init__(self, config_path='config/config.yaml'):
        self.config = Config(config_path)
        self.setup_driver()
        self.setup_logging()
        self.articles = []

    def setup_driver(self):
        chrome_options = Options()
        if self.config.headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(service=self.config.get_service(), options=chrome_options)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
        self.wait = WebDriverWait(self.driver, self.config.timeout)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def wait_for_page_load(self):
        try:
            # Wait for initial page load
            time.sleep(5)
            
            # Print page source for debugging
            page_source = self.driver.page_source
            self.logger.info(f"Page source length: {len(page_source)}")
            
            # Print all elements with class containing 'Pagination'
            elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='Pagination']")
            self.logger.info(f"Found {len(elements)} pagination elements")
            for elem in elements:
                self.logger.info(f"Pagination element class: {elem.get_attribute('class')}")
            
            # Print all elements with class containing 'Hit'
            hits = self.driver.find_elements(By.CSS_SELECTOR, "[class*='Hit']")
            self.logger.info(f"Found {len(hits)} hit elements")
            for hit in hits:
                self.logger.info(f"Hit element class: {hit.get_attribute('class')}")
            
            # Switch to the main window if multiple windows exist
            if len(self.driver.window_handles) > 0:
                self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Wait for body element
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for page to be fully loaded
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for any dynamic content
            time.sleep(2)
            
            return True
        except Exception as e:
            self.logger.error(f"Page load error: {str(e)}")
            return False

    def scroll_page(self):
        try:
            # Get initial height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down gradually
                for i in range(10):
                    self.driver.execute_script(f"window.scrollTo(0, {(i+1) * last_height/10});")
                    time.sleep(0.2)
                
                # Wait for content to load
                time.sleep(2)
                
                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # Break if no more content
                if new_height == last_height:
                    break
                    
                last_height = new_height
                
            self.logger.info("Finished scrolling")
            
        except Exception as e:
            self.logger.error(f"Scrolling error: {str(e)}")

    def extract_articles(self):
        try:
            # Wait for articles to load
            time.sleep(3)
            
            # Find all article elements with the search hit class
            articles = self.driver.find_elements(By.CLASS_NAME, "_searchHit_qg6i7_1")
            self.logger.info(f"Found {len(articles)} articles")
            
            for article in articles:
                try:
                    # Extract article data
                    link_elem = article.find_element(By.TAG_NAME, "a")
                    title = link_elem.text.strip()
                    url = link_elem.get_attribute("href")
                    
                    # Only add if we have both title and URL
                    if title and url:
                        self.articles.append({
                            "title": title,
                            "url": url,
                            "date": datetime.now().strftime("%Y-%m-%d")
                        })
                        self.logger.info(f"Added article: {title}")
                except Exception as e:
                    self.logger.debug(f"Error extracting article: {str(e)}")
                    continue
            
            if not self.articles:
                self.logger.error("No articles found")
                
        except Exception as e:
            self.logger.error(f"Article extraction error: {str(e)}")

    def click_next_page(self, page_number):
        try:
            # Wait for pagination to be present
            time.sleep(3)
            
            # Find the next page number link
            next_page = str(page_number + 1)
            
            # Look for the page number element
            xpath_expressions = [
                f"//a[text()='{next_page}']",  # Direct number match
                f"//button[text()='{next_page}']",  # Button with number
                f"//span[text()='{next_page}']/parent::a",  # Number within span
                f"//div[contains(@class, 'pagination')]//a[text()='{next_page}']"  # Within pagination div
            ]
            
            for xpath in xpath_expressions:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    self.logger.info(f"Found {len(elements)} elements for xpath: {xpath}")
                    
                    for element in elements:
                        if element.is_displayed():
                            # Scroll element into view
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            time.sleep(1)
                            
                            # Try clicking
                            try:
                                element.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", element)
                            
                            # Wait for page to load
                            time.sleep(2)
                            
                            # Verify page changed by checking URL or content
                            if self.verify_page_changed():
                                self.logger.info(f"Successfully navigated to page {next_page}")
                                return True
                except Exception as e:
                    self.logger.debug(f"Failed with xpath {xpath}: {str(e)}")
                    continue
            
            self.logger.info("Could not find next page link")
            return False
            
        except Exception as e:
            self.logger.error(f"Next page error: {str(e)}")
            return False

    def verify_page_changed(self):
        try:
            # Wait for new content to load
            time.sleep(2)
            
            # Get current articles
            current_articles = self.driver.find_elements(By.CLASS_NAME, "_searchHit_qg6i7_1")
            
            # Check if we have articles
            return len(current_articles) > 0
            
        except Exception as e:
            self.logger.error(f"Page verification error: {str(e)}")
            return False

    def save_to_csv(self, filename):
        try:
            if not self.articles:
                raise Exception("No data to save")
                
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save to CSV
            df = pd.DataFrame(self.articles)
            df.to_csv(filename, index=False)
            self.logger.info(f"Saved {len(self.articles)} articles to {filename}")
            
        except Exception as e:
            self.logger.error(f"Save error: {str(e)}")

    def run_scraper(self, url, output_name, max_pages=10):
        try:
            # Navigate to URL
            self.driver.get(url)
            self.logger.info("Navigated to URL")
            
            # Wait for initial page load
            if not self.wait_for_page_load():
                raise Exception("Initial page load failed")
            
            page = 1
            while page <= max_pages:
                try:
                    # Extract articles from current page
                    self.logger.info(f"Extracting page {page}")
                    self.extract_articles()
                    
                    # Try to go to next page if not on last page
                    if page < max_pages:
                        if not self.click_next_page(page):
                            self.logger.info("No more pages available")
                            break
                        page += 1
                    else:
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error on page {page}: {str(e)}")
                    break
            
            # Save results
            self.save_to_csv(output_name)
            
        except Exception as e:
            self.logger.error(f"Scraping error: {str(e)}")
        finally:
            self.driver.quit()
            self.logger.info("Scraping completed")

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.run_scraper(
        url="https://discover.abc.net.au/index.html?siteTitle=news#/?query=global&refinementList%5Bsite.title%5D%5B0%5D=ABC%20News",
        output_name="abc_news_articles.csv"
    )