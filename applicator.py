import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from profile import PROFILE

class JobApplicator:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def apply_easy_apply(self, job, cover_letter):
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Application took too long")
        
        # Set 60 second timeout for entire application
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(60)
        
        try:
            self.driver.get(job['url'])
            time.sleep(2)
            
            # Check if already applied - look for Applied badge/status
            try:
                page_text = self.driver.page_source
                if 'Applied' in page_text and ('ago' in page_text or 'See application' in page_text):
                    print("  ⏭️  LinkedIn shows already applied - skipping")
                    return 'already_applied'
            except:
                pass
            
            # Click Easy Apply button
            try:
                easy_apply_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.jobs-apply-button'))
                )
                easy_apply_btn.click()
                time.sleep(2)
            except:
                print("  ⚠️  No Easy Apply button - skipping")
                return False
            
            # Fill form fields
            self._fill_contact_info()
            self._fill_cover_letter(cover_letter)
            
            # Navigate through multi-step forms
            max_steps = 5
            for step in range(max_steps):
                if self._check_review_page():
                    break
                
                # Fill any additional questions on this page
                self._fill_additional_questions()
                time.sleep(1)
                
                if not self._click_next():
                    break
                time.sleep(2)
            
            # Submit
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Submit"]')
            submit_btn.click()
            time.sleep(2)
            
            signal.alarm(0)  # Cancel timeout
            return True
        except TimeoutError:
            print("  ⏱️  Application timed out (stuck on questions) - marked as partial")
            signal.alarm(0)
            return 'partial'
        except Exception as e:
            print(f"  ❌ Application failed: {str(e)[:50]}")
            signal.alarm(0)
            return False
    
    def _fill_contact_info(self):
        fields = {
            'phone': PROFILE['phone'],
            'email': PROFILE['email']
        }
        for field_type, value in fields.items():
            try:
                input_field = self.driver.find_element(By.CSS_SELECTOR, f'input[type*="{field_type}"]')
                input_field.clear()
                input_field.send_keys(value)
            except:
                pass
        
        # Fill common additional questions
        self._fill_additional_questions()
    
    def _fill_additional_questions(self):
        """Auto-fill common screening questions"""
        try:
            # Years of experience - look for number inputs
            number_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="number"]')
            for inp in number_inputs:
                label_text = inp.get_attribute('aria-label') or ''
                if 'year' in label_text.lower() or 'experience' in label_text.lower():
                    inp.clear()
                    inp.send_keys('10')  # 10+ years experience
            
            # Radio buttons - select "Yes" for authorization/sponsorship
            radios = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            for radio in radios:
                label = radio.get_attribute('aria-label') or radio.get_attribute('value') or ''
                if 'yes' in label.lower() or 'authorized' in label.lower():
                    radio.click()
                    break
            
            # Dropdowns - select first valid option
            selects = self.driver.find_elements(By.CSS_SELECTOR, 'select')
            for select in selects:
                options = select.find_elements(By.TAG_NAME, 'option')
                if len(options) > 1:
                    options[1].click()  # Skip placeholder, select first real option
        except:
            pass
    
    def _fill_cover_letter(self, cover_letter):
        try:
            textarea = self.driver.find_element(By.CSS_SELECTOR, 'textarea')
            textarea.send_keys(cover_letter)
        except:
            pass
    
    def _click_next(self):
        try:
            next_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Continue"], button[aria-label*="Next"]')
            next_btn.click()
            return True
        except:
            return False
    
    def _check_review_page(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Submit"]')
            return True
        except:
            return False
