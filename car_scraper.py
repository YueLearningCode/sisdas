"""
Unified Car Data Web Scraper
Supports: OLX.id, Carsome.id, Mobil123, Oto.com
Output: CSV & JSON
"""

import os
import json
import csv
import time
import requests
from datetime import datetime
from typing import List, Dict, Any
from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CarScraperBase(ABC):
    """Abstract base class for car scrapers"""
    
    def __init__(self, website_name: str):
        self.website_name = website_name
        self.cars_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def scrape(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """Scrape car data from website"""
        pass
    
    def get_data(self) -> List[Dict[str, Any]]:
        """Return scraped data"""
        return self.cars_data
    
    def save_to_csv(self, filename: str):
        """Save data to CSV"""
        if not self.cars_data:
            logger.warning(f"No data to save for {self.website_name}")
            return
        
        keys = set()
        for car in self.cars_data:
            keys.update(car.keys())
        
        keys = sorted(list(keys))
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.cars_data)
            logger.info(f"Saved {len(self.cars_data)} records to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def save_to_json(self, filename: str):
        """Save data to JSON"""
        if not self.cars_data:
            logger.warning(f"No data to save for {self.website_name}")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.cars_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.cars_data)} records to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


class OLXScraper(CarScraperBase):
    """Scraper for OLX.id using internal API"""
    
    def __init__(self):
        super().__init__("OLX.id")
        self.base_url = "https://www.olx.co.id/api/v1/items"
        self.category_id = "2000"  # Cars category
    
    def scrape(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """Scrape from OLX API"""
        logger.info(f"Starting OLX.id scrape (target: {max_items} items)")
        
        params = {
            'categoryId': self.category_id,
            'limit': 30,
            'offset': 0,
            'sort': '-relevance'
        }
        
        try:
            while len(self.cars_data) < max_items:
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if 'data' not in data or not data['data']:
                    logger.info("No more items available from OLX")
                    break
                
                for item in data['data']:
                    if len(self.cars_data) >= max_items:
                        break
                    
                    try:
                        car = self._parse_olx_item(item)
                        self.cars_data.append(car)
                    except Exception as e:
                        logger.debug(f"Error parsing OLX item: {e}")
                        continue
                
                params['offset'] += params['limit']
                time.sleep(1)  # Rate limiting
        
        except Exception as e:
            logger.error(f"Error scraping OLX: {e}")
        
        logger.info(f"OLX.id scrape complete: {len(self.cars_data)} items collected")
        return self.cars_data
    
    def _parse_olx_item(self, item: Dict) -> Dict[str, Any]:
        """Parse OLX item to standard format"""
        try:
            photo = item.get('photos', [{}])[0] if item.get('photos') else {}
            
            car = {
                'source': 'OLX.id',
                'car_name': item.get('title', ''),
                'brand': self._extract_brand(item.get('title', '')),
                'year': self._extract_year(item.get('title', '')),
                'mileage_km': self._extract_mileage(item.get('title', '')),
                'location': item.get('location', {}).get('city', ''),
                'transmission': self._extract_feature(item.get('title', ''), 'transmission'),
                'plate_type': '',
                'price_rp': item.get('price', 0),
                'url': f"https://www.olx.co.id/item/{item.get('id', '')}",
                'scraped_at': datetime.now().isoformat()
            }
            return car
        except Exception as e:
            logger.debug(f"Error parsing OLX item: {e}")
            raise
    
    @staticmethod
    def _extract_brand(title: str) -> str:
        """Extract car brand from title"""
        brands = ['Toyota', 'Honda', 'BMW', 'Mercedes', 'Mitsubishi', 'Nissan', 
                  'Suzuki', 'Daihatsu', 'Isuzu', 'Mazda', 'Kia', 'Hyundai', 'Ford', 'Chevrolet']
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        return ''
    
    @staticmethod
    def _extract_year(title: str) -> str:
        """Extract year from title"""
        import re
        years = re.findall(r'\b(19|20)\d{2}\b', title)
        return years[0] if years else ''
    
    @staticmethod
    def _extract_mileage(title: str) -> str:
        """Extract mileage from title"""
        import re
        mileage = re.findall(r'(\d+(?:\.\d+)?)\s*km', title.lower())
        return mileage[0] if mileage else ''
    
    @staticmethod
    def _extract_feature(text: str, feature: str) -> str:
        """Extract feature mention from text"""
        if feature.lower() in text.lower():
            return 'Yes'
        return ''


class CarSomeScraper(CarScraperBase):
    """Scraper for Carsome.id using Playwright (JavaScript-heavy)"""
    
    def __init__(self):
        super().__init__("Carsome.id")
        self.base_url = "https://www.carsome.id"
    
    def scrape(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """Scrape Carsome with Playwright"""
        logger.info(f"Starting Carsome.id scrape (target: {max_items} items)")
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                page.goto(f"{self.base_url}/cars", wait_until="networkidle")
                
                # Wait for car listings to load
                page.wait_for_selector(".car-card, [data-test-id*='car']", timeout=10000)
                
                # Get listings
                cars = page.query_selector_all(".car-card, [class*='car-item']")
                
                for car_element in cars:
                    if len(self.cars_data) >= max_items:
                        break
                    
                    try:
                        car_data = self._parse_carsome_element(car_element)
                        self.cars_data.append(car_data)
                    except Exception as e:
                        logger.debug(f"Error parsing Carsome element: {e}")
                        continue
                
                browser.close()
        
        except ImportError:
            logger.warning("Playwright not installed. Install with: pip install playwright")
        except Exception as e:
            logger.error(f"Error scraping Carsome: {e}")
        
        logger.info(f"Carsome.id scrape complete: {len(self.cars_data)} items collected")
        return self.cars_data
    
    def _parse_carsome_element(self, element) -> Dict[str, Any]:
        """Parse Carsome element to standard format"""
        try:
            title = element.text_content().split('\n')[0] if element.text_content() else ''
            
            car = {
                'source': 'Carsome.id',
                'car_name': title,
                'brand': self._extract_brand(title),
                'year': '',
                'mileage_km': '',
                'location': '',
                'transmission': '',
                'plate_type': '',
                'price_rp': 0,
                'url': element.get_attribute('href') or '',
                'scraped_at': datetime.now().isoformat()
            }
            return car
        except Exception as e:
            logger.debug(f"Error parsing Carsome element: {e}")
            raise
    
    @staticmethod
    def _extract_brand(title: str) -> str:
        """Extract brand from title"""
        brands = ['Toyota', 'Honda', 'BMW', 'Mercedes', 'Mitsubishi', 'Nissan', 
                  'Suzuki', 'Daihatsu', 'Isuzu', 'Mazda', 'Kia', 'Hyundai']
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        return ''


class Mobil123Scraper(CarScraperBase):
    """Scraper for Mobil123 using BeautifulSoup"""
    
    def __init__(self):
        super().__init__("Mobil123")
        self.base_url = "https://www.mobil123.com"
    
    def scrape(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """Scrape Mobil123"""
        logger.info(f"Starting Mobil123 scrape (target: {max_items} items)")
        
        try:
            from bs4 import BeautifulSoup
            
            page_num = 1
            
            while len(self.cars_data) < max_items:
                try:
                    url = f"{self.base_url}/listing?page={page_num}"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find car listings (adjust selectors based on actual HTML structure)
                    car_elements = soup.find_all(class_=['car-item', 'listing-item', 'product-item'])
                    
                    if not car_elements:
                        logger.info("No more listings found on Mobil123")
                        break
                    
                    for element in car_elements:
                        if len(self.cars_data) >= max_items:
                            break
                        
                        try:
                            car_data = self._parse_mobil123_element(element)
                            self.cars_data.append(car_data)
                        except Exception as e:
                            logger.debug(f"Error parsing Mobil123 element: {e}")
                            continue
                    
                    page_num += 1
                    time.sleep(1)
                
                except Exception as e:
                    logger.error(f"Error scraping Mobil123 page {page_num}: {e}")
                    break
        
        except ImportError:
            logger.warning("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        except Exception as e:
            logger.error(f"Error scraping Mobil123: {e}")
        
        logger.info(f"Mobil123 scrape complete: {len(self.cars_data)} items collected")
        return self.cars_data
    
    def _parse_mobil123_element(self, element) -> Dict[str, Any]:
        """Parse Mobil123 element"""
        try:
            title_elem = element.find(['h2', 'h3', 'a'])
            title = title_elem.text.strip() if title_elem else ''
            
            price_elem = element.find(class_=['price', 'harga'])
            price_text = price_elem.text.strip() if price_elem else '0'
            
            car = {
                'source': 'Mobil123',
                'car_name': title,
                'brand': self._extract_brand(title),
                'year': '',
                'mileage_km': '',
                'location': '',
                'transmission': '',
                'plate_type': '',
                'price_rp': self._parse_price(price_text),
                'url': element.get('href', '') if element.name == 'a' else '',
                'scraped_at': datetime.now().isoformat()
            }
            return car
        except Exception as e:
            logger.debug(f"Error parsing Mobil123 element: {e}")
            raise
    
    @staticmethod
    def _extract_brand(title: str) -> str:
        brands = ['Toyota', 'Honda', 'BMW', 'Mercedes', 'Mitsubishi', 'Nissan', 
                  'Suzuki', 'Daihatsu', 'Isuzu', 'Mazda', 'Kia', 'Hyundai']
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        return ''
    
    @staticmethod
    def _parse_price(price_str: str) -> int:
        """Parse price string to integer"""
        import re
        numbers = re.findall(r'\d+', price_str.replace('.', '').replace(',', ''))
        return int(numbers[0]) if numbers else 0


class OtoComScraper(CarScraperBase):
    """Scraper for Oto.com with deep crawling"""
    
    def __init__(self):
        super().__init__("Oto.com")
        self.base_url = "https://www.oto.com"
    
    def scrape(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """Scrape Oto.com with deep crawling"""
        logger.info(f"Starting Oto.com scrape (target: {max_items} items)")
        
        try:
            from bs4 import BeautifulSoup
            
            # First, get listings page
            response = requests.get(f"{self.base_url}/mobil", headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find car listing links
            car_links = soup.find_all('a', class_=['car-link', 'listing-link'])
            
            for link in car_links:
                if len(self.cars_data) >= max_items:
                    break
                
                try:
                    href = link.get('href', '')
                    if href:
                        # Deep crawl - go into detail page
                        car_data = self._scrape_detail_page(href)
                        if car_data:
                            self.cars_data.append(car_data)
                    
                    time.sleep(0.5)
                
                except Exception as e:
                    logger.debug(f"Error scraping Oto.com detail: {e}")
                    continue
        
        except ImportError:
            logger.warning("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        except Exception as e:
            logger.error(f"Error scraping Oto.com: {e}")
        
        logger.info(f"Oto.com scrape complete: {len(self.cars_data)} items collected")
        return self.cars_data
    
    def _scrape_detail_page(self, detail_url: str) -> Dict[str, Any]:
        """Scrape detailed info from individual car page"""
        try:
            from bs4 import BeautifulSoup
            
            full_url = detail_url if detail_url.startswith('http') else f"{self.base_url}{detail_url}"
            response = requests.get(full_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find(['h1', 'h2'])
            title_text = title.text.strip() if title else ''
            
            specs = {}
            spec_elements = soup.find_all(class_=['spec', 'specification', 'detail-item'])
            
            for spec in spec_elements:
                label = spec.find(class_=['label', 'key'])
                value = spec.find(class_=['value', 'content'])
                if label and value:
                    specs[label.text.strip().lower()] = value.text.strip()
            
            car = {
                'source': 'Oto.com',
                'car_name': title_text,
                'brand': self._extract_brand(title_text),
                'year': specs.get('tahun', specs.get('year', '')),
                'mileage_km': specs.get('km', specs.get('mileage', '')),
                'location': specs.get('lokasi', specs.get('location', '')),
                'transmission': specs.get('transmisi', specs.get('transmission', '')),
                'plate_type': specs.get('tipe plat', specs.get('plate type', '')),
                'rear_camera': specs.get('rear camera', ''),
                'sun_roof': specs.get('sun roof', ''),
                'auto_retract_mirror': specs.get('auto retract mirror', ''),
                'electric_parking_brake': specs.get('electric parking brake', ''),
                'map_navigator': specs.get('map navigator', ''),
                'vehicle_stability_control': specs.get('vehicle stability control', ''),
                'keyless_push_start': specs.get('keyless push start', ''),
                'sports_mode': specs.get('sports mode', ''),
                '360_camera_view': specs.get('360 camera', ''),
                'power_sliding_door': specs.get('power sliding door', ''),
                'auto_cruise_control': specs.get('cruise control', ''),
                'price_rp': self._extract_price(specs),
                'url': full_url,
                'scraped_at': datetime.now().isoformat()
            }
            return car
        
        except Exception as e:
            logger.debug(f"Error scraping detail page: {e}")
            return None
    
    @staticmethod
    def _extract_brand(title: str) -> str:
        brands = ['Toyota', 'Honda', 'BMW', 'Mercedes', 'Mitsubishi', 'Nissan', 
                  'Suzuki', 'Daihatsu', 'Isuzu', 'Mazda', 'Kia', 'Hyundai']
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        return ''
    
    @staticmethod
    def _extract_price(specs: Dict) -> int:
        """Extract price from specs"""
        import re
        price_candidates = [specs.get('harga', ''), specs.get('price', '')]
        for price_str in price_candidates:
            if price_str:
                numbers = re.findall(r'\d+', str(price_str).replace('.', '').replace(',', ''))
                if numbers:
                    return int(numbers[0])
        return 0


class CarScraperManager:
    """Manages multiple scrapers and data aggregation"""
    
    def __init__(self):
        self.scrapers = {
            'olx': OLXScraper(),
            'carsome': CarSomeScraper(),
            'mobil123': Mobil123Scraper(),
            'oto': OtoComScraper()
        }
        self.all_data = []
    
    def scrape_all(self, targets: List[str], max_items_per_site: int = 100):
        """Scrape from multiple sources"""
        for target in targets:
            if target.lower() in self.scrapers:
                scraper = self.scrapers[target.lower()]
                logger.info(f"Starting {target}...")
                data = scraper.scrape(max_items_per_site)
                self.all_data.extend(data)
                logger.info(f"Collected {len(data)} items from {target}")
    
    def save_all(self, output_dir: str = '.'):
        """Save all data to CSV and JSON"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save combined data
        csv_file = os.path.join(output_dir, f'cars_combined_{timestamp}.csv')
        json_file = os.path.join(output_dir, f'cars_combined_{timestamp}.json')
        
        if self.all_data:
            keys = set()
            for car in self.all_data:
                keys.update(car.keys())
            keys = sorted(list(keys))
            
            try:
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(self.all_data)
                logger.info(f"Saved combined data to {csv_file}")
            except Exception as e:
                logger.error(f"Error saving CSV: {e}")
            
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(self.all_data, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved combined data to {json_file}")
            except Exception as e:
                logger.error(f"Error saving JSON: {e}")
    
    def get_summary(self) -> str:
        """Get scraping summary"""
        summary = f"\n{'='*50}\n"
        summary += f"SCRAPING SUMMARY\n"
        summary += f"{'='*50}\n"
        summary += f"Total items scraped: {len(self.all_data)}\n"
        
        sources = {}
        for item in self.all_data:
            source = item.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        for source, count in sources.items():
            summary += f"  {source}: {count} items\n"
        
        summary += f"{'='*50}\n"
        return summary


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Car Data Web Scraper')
    parser.add_argument('--websites', nargs='+', default=['olx', 'carsome', 'mobil123', 'oto'],
                        help='Websites to scrape: olx, carsome, mobil123, oto')
    parser.add_argument('--max-items', type=int, default=1000,
                        help='Max items per website (default: 1000)')
    parser.add_argument('--output', default='./scraped_data',
                        help='Output directory (default: ./scraped_data)')
    
    args = parser.parse_args()
    
    logger.info("Starting Car Data Web Scraper...")
    logger.info(f"Targets: {args.websites}")
    logger.info(f"Max items per site: {args.max_items}")
    
    manager = CarScraperManager()
    manager.scrape_all(args.websites, args.max_items)
    manager.save_all(args.output)
    
    print(manager.get_summary())
    logger.info("Scraping complete!")


if __name__ == '__main__':
    main()
