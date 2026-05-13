# Car Data Web Scraper Documentation

## Overview
Unified Python web scraper for collecting car data from multiple Indonesian automotive websites:
- **OLX.id** - Uses internal API (XHR) for reliable JSON data
- **Carsome.id** - Playwright-based for JavaScript-heavy dynamic content
- **Mobil123** - BeautifulSoup for organized HTML structure  
- **Oto.com** - Deep crawling with detail page scraping

## Data Fields Collected
1. **car_name** - Full car name/model
2. **brand** - Car manufacturer
3. **year** - Manufacturing year
4. **mileage_km** - Mileage in kilometers
5. **location** - City/location
6. **transmission** - Manual/Automatic
7. **plate_type** - License plate type
8. **rear_camera** - Has rear camera
9. **sun_roof** - Has sun roof
10. **auto_retract_mirror** - Auto-retractable mirrors
11. **electric_parking_brake** - Electric parking brake
12. **map_navigator** - GPS/Navigation system
13. **vehicle_stability_control** - VSC/ESC system
14. **keyless_push_start** - Keyless entry/push start
15. **sports_mode** - Sport mode available
16. **360_camera_view** - 360-degree camera
17. **power_sliding_door** - Power sliding doors
18. **auto_cruise_control** - Adaptive cruise control
19. **price_rp** - Price in Indonesian Rupiah
20. **instalment_rp_monthly** - Monthly installment (if available)

## Installation

### 1. Install Dependencies
```bash
pip install -r scraper_requirements.txt
```

### 2. Setup Playwright (for Carsome.id)
```bash
# Windows
python -m playwright install chromium

# Or run without installing if you prefer
# The script will handle it automatically
```

## Usage

### Basic Usage - Scrape All Sources
```bash
python car_scraper.py
```

This will:
- Scrape 100 items from each website (default)
- Output to `./scraped_data` directory
- Save as both CSV and JSON

### Advanced Usage

#### Scrape Specific Websites
```bash
python car_scraper.py --websites olx mobil123
```

#### Scrape More Items
```bash
python car_scraper.py --max-items 500
```

#### Specify Output Directory
```bash
python car_scraper.py --output ./my_data
```

#### Combine Options
```bash
python car_scraper.py --websites oto carsome --max-items 250 --output ./results
```

## Website-Specific Information

### OLX.id
- **Method**: Internal REST API
- **Advantages**: Most reliable, returns clean JSON
- **Limitations**: May have rate limiting
- **Data Quality**: High - direct from API

### Carsome.id
- **Method**: Playwright (headless browser)
- **Advantages**: Handles JavaScript rendering
- **Limitations**: Slower, requires more resources
- **Data Quality**: Good - prices from rendered DOM

### Mobil123
- **Method**: BeautifulSoup HTML parsing
- **Advantages**: Fast, lightweight
- **Limitations**: Depends on HTML structure stability
- **Data Quality**: Medium - varies with page updates

### Oto.com
- **Method**: Multi-level crawling (listing + details)
- **Advantages**: Most detailed specifications
- **Limitations**: Slowest due to deep crawling
- **Data Quality**: Excellent - includes all specs

## Output Files

The scraper generates:
```
scraped_data/
├── cars_combined_20240513_143022.csv
└── cars_combined_20240513_143022.json
```

### CSV Format
- Headers: All unique fields from all sources
- UTF-8 encoded
- Proper handling of special characters

### JSON Format
- Pretty-printed with 2-space indentation
- Preserves Unicode characters
- Maintains data types

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'playwright'"
**Solution**: 
```bash
pip install playwright
python -m playwright install chromium
```

### Issue: "ModuleNotFoundError: No module named 'bs4'"
**Solution**: 
```bash
pip install beautifulsoup4
```

### Issue: Slow scraping from Carsome.id
**Solution**: 
- This is normal - Playwright launches a real browser
- Use `--websites olx mobil123 oto` to skip Carsome if time is critical
- Or increase `--max-items` and let it run longer

### Issue: Empty results from a website
**Solutions**:
1. Website may have changed HTML structure - check browser's Elements tab
2. Website may have blocking/CAPTCHA - try again later
3. May need proxy/VPN for some regions
4. Check logs for specific error messages

## Logging

The scraper logs all operations to console:
```
2024-05-13 14:30:22 - __main__ - INFO - Starting Car Data Web Scraper...
2024-05-13 14:30:22 - __main__ - INFO - Starting OLX.id scrape (target: 100 items)
...
```

## Customization Guide

### Adding New Website

1. Create new scraper class:
```python
class NewSiteScraper(CarScraperBase):
    def __init__(self):
        super().__init__("NewSite.com")
        self.base_url = "https://www.newsite.com"
    
    def scrape(self, max_items: int = 100) -> List[Dict[str, Any]]:
        # Your scraping logic here
        pass
```

2. Register in `CarScraperManager`:
```python
self.scrapers = {
    ...
    'newsite': NewSiteScraper(),
}
```

### Modifying Data Fields

Edit the car data dictionaries in `_parse_*` methods:
```python
car = {
    'your_field': value,
    'another_field': another_value,
}
```

## Performance Tips

1. **Reduce Carsome scraping**: Playwright is slowest
   ```bash
   python car_scraper.py --websites olx mobil123 oto --max-items 300
   ```

2. **Use smaller batches**: Test with 10 items first
   ```bash
   python car_scraper.py --max-items 10
   ```

3. **Parallelize if needed**: Modify manager to run scrapers concurrently
   ```python
   # For advanced users - implement threading
   ```

4. **Target specific sites for different data**:
   - Speed: Use `--websites olx mobil123`
   - Detail: Use `--websites oto`
   - Balance: Use `--websites olx mobil123`

## Legal & Ethical Considerations

- Always check website ToS before scraping
- Use appropriate rate limiting (built-in with `time.sleep()`)
- Respect `robots.txt` files
- Consider contacting websites for API access
- Don't overload servers with too many concurrent requests

## For 3000 Items Target

To scrape your target of 3000 items:
```bash
python car_scraper.py --max-items 750
# This will get 750 items × 4 websites = 3000 total items

# Or scrape more from specific sites:
python car_scraper.py --websites olx mobil123 --max-items 1500
```

## Troubleshooting API Changes

If a website changes its structure:

1. **Check with your browser**:
   - Open website
   - Press F12 (Developer Tools)
   - Inspect HTML elements
   - Check Network tab for API calls (XHR)

2. **Update CSS selectors** in the scraper to match new structure

3. **For API-based sites**: Check if they provide official API documentation

## Support

For issues:
1. Check logs for error messages
2. Verify internet connection
3. Try again later (may be temporary blocks)
4. Inspect website structure changes
5. Test with `--max-items 10` first

---

**Last Updated**: May 13, 2024
**Version**: 1.0
