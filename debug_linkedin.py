#!/usr/bin/env python3
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# Setup browser
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # Login
    print("Logging into LinkedIn...")
    driver.get('https://www.linkedin.com/login')
    driver.find_element(By.ID, 'username').send_keys(os.getenv('LINKEDIN_EMAIL'))
    driver.find_element(By.ID, 'password').send_keys(os.getenv('LINKEDIN_PASSWORD'))
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(3)
    
    # Search for jobs
    print("Searching for Cloud Engineer jobs...")
    driver.get('https://www.linkedin.com/jobs/search/?keywords=Cloud%20Engineer&location=Remote&f_AL=true')
    time.sleep(5)
    
    # Save page source
    with open('linkedin_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    print("\n✓ Page source saved to linkedin_page.html")
    print("\nNow I'll try to find job cards...")
    
    # Try different selectors
    selectors = [
        'li.jobs-search-results__list-item',
        '.job-card-container',
        '.jobs-search-results__list-item',
        'li[data-occludable-job-id]',
        '.scaffold-layout__list-item'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"✓ Found {len(elements)} elements with: {selector}")
            else:
                print(f"✗ No elements with: {selector}")
        except Exception as e:
            print(f"✗ Error with {selector}: {e}")
    
    print("\nLeaving browser open for 30 seconds so you can inspect...")
    print("Check the Elements tab in browser DevTools")
    time.sleep(30)
    
finally:
    driver.quit()
