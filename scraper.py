"""
Web scraper module for extracting product data from books.toscrape.com
"""
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin


class ProductScraper:
    """Scraper for books.toscrape.com"""
    
    BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
    MAIN_URL = "https://books.toscrape.com"
    
    # Rating mapping
    RATING_MAP = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    
    def __init__(self, rate_limit: float = 1.0, max_retries: int = 3):
        """
        Initialize the scraper
        
        Args:
            rate_limit: Delay between requests in seconds
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic and exponential backoff
        
        Args:
            url: URL to fetch
            
        Returns:
            Response object or None if all retries failed
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    wait_time = (2 ** attempt) * self.rate_limit
                    print(f"Request failed, retrying in {wait_time}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"Failed to fetch {url} after {self.max_retries} attempts: {e}")
                    return None
        return None
    
    def _extract_rating(self, article) -> Optional[int]:
        """Extract rating from product article element"""
        rating_element = article.find('p', class_='star-rating')
        if rating_element:
            for rating_text, rating_value in self.RATING_MAP.items():
                if rating_text in rating_element.get('class', []):
                    return rating_value
        return None
    
    def _extract_price(self, article) -> Optional[str]:
        """Extract price from product article element"""
        price_element = article.find('p', class_='price_color')
        if price_element:
            return price_element.text.strip()
        return None
    
    def _extract_availability(self, article) -> str:
        """Extract availability status from product article element"""
        availability_element = article.find('p', class_='instock availability')
        if availability_element:
            return availability_element.text.strip()
        return "Unknown"
    
    def _extract_product_url(self, article) -> Optional[str]:
        """Extract product page URL from article element"""
        h3_element = article.find('h3')
        if h3_element:
            a_element = h3_element.find('a')
            if a_element and a_element.get('href'):
                # Convert relative URL to absolute
                relative_url = a_element['href']
                # Remove '../../../' prefix if present
                relative_url = relative_url.replace('../../../', 'catalogue/')
                return urljoin(self.MAIN_URL, relative_url)
        return None
    
    def _extract_title(self, article) -> Optional[str]:
        """Extract product title from article element"""
        h3_element = article.find('h3')
        if h3_element:
            a_element = h3_element.find('a')
            if a_element:
                return a_element.get('title', a_element.text.strip())
        return None
    
    def scrape_page(self, page_number: int) -> List[Dict[str, any]]:
        """
        Scrape a single page of product listings
        
        Args:
            page_number: Page number to scrape
            
        Returns:
            List of product dictionaries
        """
        if page_number == 1:
            url = "https://books.toscrape.com/index.html"
        else:
            url = self.BASE_URL.format(page_number)
        
        print(f"Scraping page {page_number}: {url}")
        
        # Rate limiting
        time.sleep(self.rate_limit)
        
        response = self._make_request(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Find all product articles
        articles = soup.find_all('article', class_='product_pod')
        
        for article in articles:
            product = {
                'title': self._extract_title(article),
                'price': self._extract_price(article),
                'rating': self._extract_rating(article),
                'availability': self._extract_availability(article),
                'url': self._extract_product_url(article)
            }
            
            # Only add if we have at least title and price
            if product['title'] and product['price']:
                products.append(product)
        
        print(f"Found {len(products)} products on page {page_number}")
        return products
    
    def scrape_multiple_pages(self, num_pages: int, progress_callback=None) -> List[Dict[str, any]]:
        """
        Scrape multiple pages of product listings
        
        Args:
            num_pages: Number of pages to scrape
            progress_callback: Optional callback function(current, total, message)
            
        Returns:
            List of all product dictionaries from all pages
        """
        all_products = []
        
        for page_num in range(1, num_pages + 1):
            if progress_callback:
                progress_callback(page_num, num_pages, f"Scraping page {page_num}/{num_pages}...")
            
            products = self.scrape_page(page_num)
            all_products.extend(products)
            
            # Check if we got no products (might have reached the last page)
            if not products:
                print(f"No products found on page {page_num}. Stopping.")
                break
        
        return all_products
