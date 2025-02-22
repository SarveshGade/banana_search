from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium import webdriver
print(webdriver.__version__)

def get_walmart_apple_prices():
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless=new")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Open Walmart search results for apples
        url = "https://www.walmart.com/search?q=apples"
        driver.get(url)
        
        time.sleep(5)  # Allow time for dynamic content to load
        
        # Extract product details
        apple_prices = []
        products = driver.find_elements(By.CSS_SELECTOR, "div.search-result-gridview-item")
        
        for product in products[:5]:  # Limit to first 5 results
            try:
                name = product.find_element(By.CSS_SELECTOR, "span.w_V_DM").text
                price = product.find_element(By.CSS_SELECTOR, "span.price-group").text
                apple_prices.append((name, price))
            except:
                continue
        
        return apple_prices
    
    finally:
        driver.quit()

if __name__ == "__main__":
    prices = get_walmart_apple_prices()
    for name, price in prices:
        print(f"{name}: {price}")
