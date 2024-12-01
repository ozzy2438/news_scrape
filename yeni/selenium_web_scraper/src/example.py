import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.scraper import WebScraper

def scrape_abc_australia():
    """Script to scrape ABC News Australia discover page with pagination"""
    
    # Initialize the scraper with config from the config directory
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    scraper = WebScraper(config_path=config_path)
    
    # ABC News Australia discover URL with global news filter
    url = "https://discover.abc.net.au/index.html?siteTitle=news#/?query=global&refinementList%5Bsite.title%5D%5B0%5D=ABC%20News"
    
    try:
        scraper.run_scraper(
            url=url,
            output_name="output/abc_news_articles.csv",
            max_pages=10
        )
    except Exception as e:
        print(f"Error scraping ABC News Australia: {str(e)}")

if __name__ == "__main__":
    scrape_abc_australia()