import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from profile import PROFILE

class JobScraper:
    def __init__(self, email, password):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)
        self.email = email
        self.password = password
        self.wait = WebDriverWait(self.driver, 10)
        
    def login_linkedin(self):
        self.driver.get('https://www.linkedin.com/login')
        self.driver.find_element(By.ID, 'username').send_keys(self.email)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)
    
    def search_jobs(self, limit=50):
        jobs = []
        for role in PROFILE['target_roles'][:5]:  # Search top 5 roles
            if len(jobs) >= limit:
                break
            search_url = f'https://www.linkedin.com/jobs/search/?keywords={role.replace(" ", "%20")}&location=Remote&f_AL=true'
            self.driver.get(search_url)
            time.sleep(3)
            
            # Updated selectors for current LinkedIn
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, 'li[data-occludable-job-id]')[:10]
            for card in job_cards:
                if len(jobs) >= limit:
                    break
                try:
                    card.click()
                    time.sleep(3)
                    
                    # Wait for job details to load
                    title = self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '.job-details-jobs-unified-top-card__job-title')
                    )).text
                    
                    company = self.driver.find_element(By.CSS_SELECTOR, '.job-details-jobs-unified-top-card__company-name').text
                    description = self.driver.find_element(By.CSS_SELECTOR, '.jobs-description__details, .jobs-description').text
                    job_url = self.driver.current_url
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'description': description,
                        'url': job_url,
                        'source': 'LinkedIn'
                    })
                except Exception as e:
                    print(f"Skipping job: {e}")
                    continue
        
        return jobs[:limit]
    
    def close(self):
        self.driver.quit()
