import os
import sys
from urllib.parse import quote

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.scraper import WebScraper

def get_user_query():
    """Get search query from user input"""
    print("\nABC News Scraper")
    print("=" * 50)
    print("\nHangi tür query'leri scrape yapmak istiyorsunuz?")
    print("Örnek queryler:")
    print("1. climate change")
    print("2. australian politics")
    print("3. technology")
    print("4. sports")
    print("5. business")
    print("\nLütfen query'nizi girin: ")
    query = input().strip()
    
    # Convert numbered choices to actual queries
    query_map = {
        "1": "climate change",
        "2": "australian politics",
        "3": "technology",
        "4": "sports",
        "5": "business"
    }
    
    # If user entered a number, convert it to the corresponding query
    if query in query_map:
        query = query_map[query]
    
    return query

def continue_scraping():
    """Ask user if they want to continue with another query"""
    while True:
        response = input("\nBaşka bir query için devam etmek istiyor musunuz? (evet/hayır): ").strip().lower()
        if response in ['evet', 'e', 'yes', 'y']:
            return True
        elif response in ['hayır', 'h', 'no', 'n']:
            return False
        else:
            print("Lütfen 'evet' veya 'hayır' olarak cevap verin.")

def scrape_abc_australia():
    """Script to scrape ABC News Australia discover page with pagination"""
    
    while True:
        # Initialize the scraper with config from the config directory
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        scraper = WebScraper(config_path=config_path)
        
        try:
            # Get query from user
            query = get_user_query()
            
            # Create output filename based on query
            output_filename = f"output/abc_news_{query.replace(' ', '_').lower()}.csv"
            
            print(f"\nScraping başlıyor: '{query}' için arama yapılıyor...")
            
            # Run the scraper
            scraper.run_scraper(
                output_name=output_filename,
                max_pages=10
            )
            
            print(f"\nScraping tamamlandı! Sonuçlar şu dosyaya kaydedildi: {output_filename}")
            
            # Clean up the current scraper
            if hasattr(scraper, 'driver'):
                scraper.driver.quit()
            
            # Ask if user wants to continue
            if not continue_scraping():
                print("\nProgram sonlandırılıyor. İyi günler!")
                break
                
        except Exception as e:
            print(f"Error scraping ABC News Australia: {str(e)}")
            if hasattr(scraper, 'driver'):
                scraper.driver.quit()
            
            if not continue_scraping():
                print("\nProgram sonlandırılıyor. İyi günler!")
                break

if __name__ == "__main__":
    scrape_abc_australia()