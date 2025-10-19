from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime
from captcha_solver import CaptchaSolver
from pdf_generator import PDFGenerator

class DelhiCourtsScraper:
    """Scraper for Delhi District Courts Cause Lists - Multi-Browser Support"""
    
    def __init__(self, headless=False, browser="firefox"):
        self.base_url = "https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/"
        self.captcha_solver = CaptchaSolver()
        self.pdf_generator = PDFGenerator()
        self.driver = None
        self.headless = headless
        self.browser = browser.lower()
        
        # Auto-detect drivers
        self.geckodriver_path = self._find_driver("geckodriver.exe")
        self.chromedriver_path = self._find_driver("chromedriver.exe")
        
        # Create directories
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("downloads/pdfs", exist_ok=True)
        os.makedirs("downloads/captchas", exist_ok=True)
        os.makedirs("downloads/json", exist_ok=True)
    
    def _find_driver(self, driver_name):
        """Auto-detect driver exe in project folder"""
        possible_paths = [
            driver_name,
            os.path.join(os.getcwd(), driver_name),
            os.path.join(os.path.dirname(__file__), driver_name),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    def init_driver(self):
        """Initialize WebDriver - Tries Firefox first, then Chrome"""
        
        if self.browser == "firefox" or (self.browser == "auto" and self.geckodriver_path):
            try:
                return self._init_firefox()
            except Exception as e:
                print(f"⚠️  Firefox failed: {e}")
                if self.browser == "firefox":
                    raise
                print("Falling back to Chrome...")
        
        try:
            return self._init_chrome()
        except Exception as e:
            print(f"⚠️  Chrome failed: {e}")
            
            if self.browser != "firefox":
                print("Trying Firefox as last resort...")
                return self._init_firefox()
            raise
    
    def _init_firefox(self):
        """Initialize Firefox WebDriver"""
        print("🦊 Initializing Firefox...")
        
        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--disable-gpu')
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('useAutomationExtension', False)
        
        try:
            if self.geckodriver_path:
                print(f"✅ Found GeckoDriver at: {self.geckodriver_path}")
                service = FirefoxService(executable_path=self.geckodriver_path)
                self.driver = webdriver.Firefox(service=service, options=options)
            else:
                print("🔍 Trying GeckoDriver from system PATH...")
                self.driver = webdriver.Firefox(options=options)
            
            self.driver.maximize_window()
            print("✅ Firefox WebDriver initialized successfully!")
            self.browser = "firefox"
            return True
            
        except Exception as e:
            print(f"❌ Firefox initialization failed: {e}")
            raise
    
    def _init_chrome(self):
        """Initialize Chrome WebDriver"""
        print("🌐 Initializing Chrome...")
        
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless=new')
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        try:
            if self.chromedriver_path:
                print(f"✅ Found ChromeDriver at: {self.chromedriver_path}")
                service = ChromeService(executable_path=self.chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                print("🔍 Trying ChromeDriver from system PATH...")
                self.driver = webdriver.Chrome(options=options)
            
            self.driver.maximize_window()
            print("✅ Chrome WebDriver initialized successfully!")
            self.browser = "chrome"
            return True
            
        except Exception as e:
            print(f"❌ Chrome initialization failed: {e}")
            raise
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def navigate_to_page(self):
        """Navigate to the cause list page with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"🌐 Navigating to Delhi Courts website (Attempt {retry_count + 1}/{max_retries})...")
                
                self.driver.set_page_load_timeout(60)
                self.driver.get(self.base_url)
                
                WebDriverWait(self.driver, 30).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                
                print("✅ Page loaded successfully!")
                time.sleep(3)
                return True
                
            except Exception as e:
                retry_count += 1
                print(f"⚠️  Navigation attempt {retry_count} failed: {e}")
                
                if retry_count < max_retries:
                    print(f"⏳ Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("❌ All navigation attempts failed")
                    raise Exception(f"Could not load page after {max_retries} attempts")
    
    def fetch_available_courts(self):
        """Fetch list of available courts"""
        try:
            print("📋 Fetching available courts...")
            
            self.init_driver()
            
            try:
                self.navigate_to_page()
            except Exception as nav_error:
                print(f"❌ Navigation failed: {nav_error}")
                self.close_driver()
                return []
            
            print("⏳ Waiting for page elements to load...")
            time.sleep(5)
            
            try:
                print(f"📄 Page title: {self.driver.title}")
                print(f"🔗 Current URL: {self.driver.current_url}")
            except:
                pass
            
            # STEP 1: Select Court Complex
            print("\n🔍 STEP 1: Finding Court Complex dropdown...")
            court_complex_dropdown = None
            
            try:
                complex_selects = self.driver.find_elements(By.NAME, "est_code")
                
                if complex_selects:
                    court_complex_dropdown = complex_selects[0]
                    print(f"✅ Found Court Complex dropdown")
                    
                    print("🎯 Selecting 'Patiala House Court Complex'...")
                    complex_select = Select(court_complex_dropdown)
                    
                    if len(complex_select.options) > 1:
                        try:
                            complex_select.select_by_visible_text("Patiala House Court Complex")
                            print("✅ Selected 'Patiala House Court Complex'")
                        except:
                            complex_select.select_by_index(1)
                            print(f"✅ Selected by index")
                        
                        # Wait for Court Number dropdown to populate (check if it has options)
                        print("⏳ Waiting for Court Number dropdown to populate...")
                        wait_attempts = 0
                        max_wait = 10
                        
                        while wait_attempts < max_wait:
                            time.sleep(2)
                            try:
                                court_dropdown_temp = self.driver.find_element(By.NAME, "court")
                                court_select_temp = Select(court_dropdown_temp)
                                
                                # Check if dropdown has more than just "Select Court" option
                                if len(court_select_temp.options) > 1:
                                    print(f"✅ Dropdown populated with {len(court_select_temp.options)} options after {(wait_attempts + 1) * 2} seconds")
                                    break
                                else:
                                    wait_attempts += 1
                                    print(f"   Still waiting... ({wait_attempts}/{max_wait})")
                            except:
                                wait_attempts += 1
                        
                        if wait_attempts >= max_wait:
                            print("⚠️  Dropdown didn't populate after 20 seconds")
                    else:
                        print("⚠️  No court complex options found")
                else:
                    print("⚠️  Court Complex dropdown not found")
            except Exception as e:
                print(f"⚠️  Error selecting court complex: {e}")
            
            # STEP 2: Find Court Number dropdown
            print("\n🔍 STEP 2: Finding Court Number dropdown...")
            court_dropdown = None
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "court"))
                )
                
                court_dropdown = self.driver.find_element(By.NAME, "court")
                print("✅ Found Court Number dropdown")
                
            except Exception as e:
                print(f"⚠️  Could not find Court Number dropdown: {e}")
                
                try:
                    court_dropdown = self.driver.find_element(By.ID, "court")
                    print("✅ Found Court Number dropdown by ID")
                except:
                    print("❌ All strategies failed to find Court Number dropdown")
            
            if not court_dropdown:
                print("❌ Could not find court dropdown")
                self.close_driver()
                return []
            
            # STEP 3: Extract options
            print("\n🔍 STEP 3: Extracting court options...")
            select_element = Select(court_dropdown)
            options = select_element.options
            
            print(f"📊 Court Number dropdown has {len(options)} total options")
            
            courts = []
            for idx, option in enumerate(options):
                text = option.text.strip()
                value = option.get_attribute('value')
                
                if idx < 5:
                    print(f"   Option {idx}: value='{value[:50] if value else 'None'}...', text='{text[:60]}...'")
                
                if text and value and text.lower() != "select court" and text.lower() != "select court...":
                    courts.append({
                        'value': value,
                        'text': text,
                        'display': text
                    })
            
            print(f"\n✅ Found {len(courts)} available courts")
            
            if courts:
                print("📋 Sample courts:")
                for court in courts[:5]:
                    print(f"   - {court['text'][:80]}...")
            
            self.close_driver()
            
            return courts
            
        except Exception as e:
            print(f"❌ Error fetching courts: {e}")
            
            if self.driver:
                self.close_driver()
            return []
    
    def select_court_number(self, court_value):
        try:
            select_element = Select(self.driver.find_element(By.NAME, "court"))
            select_element.select_by_value(court_value)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ Error selecting court number: {e}")
            return False
    
    def enter_date(self, date_str):
        """Enter date using JavaScript (datepicker is read-only)"""
        try:
            # Date field is READ-ONLY with datepicker - use JavaScript
            date_input = self.driver.find_element(By.NAME, "date")
            
            # Set value using JavaScript (bypasses read-only restriction)
            self.driver.execute_script(f"arguments[0].value = '{date_str}';", date_input)
            
            # Trigger change event so form knows value changed
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", date_input)
            
            time.sleep(1)
            print(f"✅ Entered date: {date_str}")
            return True
        except Exception as e:
            print(f"❌ Error entering date: {e}")
            return False
    
    def select_case_type(self, case_type="civil"):
        try:
            # Use name="cause_type" with value="2" for civil, "3" for criminal
            if case_type.lower() == "civil":
                radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='cause_type'][value='2']")
            else:
                radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='cause_type'][value='3']")
            
            if not radio.is_selected():
                radio.click()
            
            time.sleep(1)
            print(f"✅ Selected {case_type} case type")
            return True
        except Exception as e:
            print(f"❌ Error selecting case type: {e}")
            return False
    
    def download_captcha_image(self):
        try:
            captcha_img = None
            selectors = [
                "img[src*='captcha']",
                "img[alt*='captcha']",
                "img[id*='captcha']",
                "#captcha_image",
                ".captcha-image"
            ]
            
            for selector in selectors:
                try:
                    captcha_img = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not captcha_img:
                captcha_container = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Captcha') or contains(text(), 'captcha')]/following::img[1]")
                captcha_img = captcha_container
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            captcha_path = f"downloads/captchas/captcha_{timestamp}.png"
            
            captcha_img.screenshot(captcha_path)
            print(f"✅ Captcha saved: {captcha_path}")
            return captcha_path
        except Exception as e:
            print(f"❌ Error downloading captcha: {e}")
            return None
    
    def solve_and_enter_captcha(self):
        try:
            captcha_path = self.download_captcha_image()
            if not captcha_path:
                return False
            
            captcha_text = self.captcha_solver.solve_with_fallback(captcha_path)
            
            captcha_input = None
            input_names = ["captcha_code", "captcha", "captchaCode", "txtCaptcha"]
            
            for name in input_names:
                try:
                    captcha_input = self.driver.find_element(By.NAME, name)
                    break
                except:
                    continue
            
            if not captcha_input:
                captcha_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter Captcha Code' or contains(@placeholder, 'Captcha')]")
            
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            
            print(f"✅ Entered captcha: {captcha_text}")
            return True
            
        except Exception as e:
            print(f"❌ Error solving captcha: {e}")
            return False
    
    def click_search(self):
        try:
            search_btn = None
            selectors = [
                "input[value='Search']",
                "button[type='submit']",
                "input[type='submit']",
                "//button[contains(text(), 'Search')]",
                "//input[contains(@value, 'Search')]"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        search_btn = self.driver.find_element(By.XPATH, selector)
                    else:
                        search_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if search_btn:
                search_btn.click()
                time.sleep(3)
                print("✅ Clicked Search button")
                return True
            else:
                print("❌ Could not find search button")
                return False
        except Exception as e:
            print(f"❌ Error clicking search: {e}")
            return False
    
    def check_if_results_loaded(self):
        try:
            results_present = len(self.driver.find_elements(By.TAG_NAME, "table")) > 0
            
            page_text = self.driver.page_source.lower()
            if "no case" in page_text or "not found" in page_text or "no records" in page_text:
                return False, "No cases found"
            
            return results_present, "Results found"
        except Exception as e:
            return False, str(e)
    
    def scrape_cause_list(self):
        try:
            page_html = self.driver.page_source
            
            court_info = {
                'timestamp': datetime.now().isoformat(),
                'url': self.driver.current_url,
                'html_content': page_html
            }
            
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            
            if tables:
                print(f"✅ Found {len(tables)} table(s) on page")
                return court_info, page_html
            else:
                print("⚠️ No tables found on page")
                return court_info, page_html
                
        except Exception as e:
            print(f"❌ Error scraping cause list: {e}")
            return None, None
    
    def go_back_to_search(self):
        try:
            back_elements = [
                (By.LINK_TEXT, "Back"),
                (By.PARTIAL_LINK_TEXT, "Back"),
            ]
            
            for by, value in back_elements:
                try:
                    back_btn = self.driver.find_element(by, value)
                    back_btn.click()
                    time.sleep(2)
                    print("✅ Navigated back to search form")
                    return True
                except:
                    continue
            
            self.driver.get(self.base_url)
            time.sleep(2)
            return True
        except:
            self.driver.get(self.base_url)
            time.sleep(2)
            return True
    
    def scrape_selected_courts(self, selected_courts, date_str, case_type="civil"):
        results = []
        
        try:
            self.init_driver()
            self.navigate_to_page()
            
            print(f"\n📋 Starting to scrape {len(selected_courts)} selected court(s)...")
            print(f"🔧 Using browser: {self.browser.upper()}")
            
            for idx, court in enumerate(selected_courts, 1):
                print(f"\n{'='*60}")
                print(f"🏛️  Processing Court {idx}/{len(selected_courts)}: {court['text']}")
                print(f"{'='*60}")
                
                try:
                    # Select court complex
                    try:
                        complex_select = Select(self.driver.find_element(By.NAME, "est_code"))
                        if len(complex_select.options) > 1:
                            complex_select.select_by_index(1)
                            print("✅ Re-selected court complex")
                            time.sleep(3)
                    except:
                        print("ℹ️  Skipped court complex re-selection")
                    
                    # Select court
                    try:
                        court_select = Select(self.driver.find_element(By.NAME, "court"))
                        court_select.select_by_value(court['value'])
                        print(f"✅ Selected court: {court['text'][:50]}...")
                        time.sleep(1)
                    except Exception as e:
                        print(f"❌ Error selecting court: {e}")
                        continue
                    
                    # Enter date
                    if not self.enter_date(date_str):
                        print("⚠️ Date entry failed, skipping")
                        continue
                    
                    # Select case type
                    self.select_case_type(case_type)
                    
                    # Solve captcha
                    if not self.solve_and_enter_captcha():
                        print("⚠️ Captcha solving failed, skipping this court")
                        self.go_back_to_search()
                        continue
                    
                    # Click search
                    self.click_search()
                    
                    # Wait for results page
                    print("⏳ Waiting for results page to load...")
                    time.sleep(5)
                    
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.TAG_NAME, "table"))
                        )
                        print("✅ Results table detected")
                    except:
                        print("⚠️  No table found")
                    
                    time.sleep(2)
                    
                    current_url = self.driver.current_url
                    print(f"📍 Current URL: {current_url}")
                    
                    # Check if results loaded
                    results_loaded, message = self.check_if_results_loaded()
                    
                    if results_loaded:
                        print("📊 Scraping cause list data...")
                        court_info, html_content = self.scrape_cause_list()
                        
                        if court_info and html_content:
                            # Check if we captured the form page by mistake
                            if "Please Enter the Captcha" in html_content or "This form needs JavaScript" in html_content:
                                print("⚠️  WARNING: Captured form page instead of results!")
                                print("💡 Waiting longer and re-capturing...")
                                time.sleep(5)
                                court_info, html_content = self.scrape_cause_list()
                            
                            pdf_filename = f"{court['text'].replace(' ', '_').replace('/', '-')}_{date_str.replace('/', '-')}_{case_type}.pdf"
                            pdf_path = self.pdf_generator.generate_pdf(
                                html_content,
                                pdf_filename,
                                court['text'],
                                date_str
                            )
                            
                            results.append({
                                'court': court['text'],
                                'date': date_str,
                                'case_type': case_type,
                                'status': 'success',
                                'pdf_path': pdf_path,
                                'info': court_info
                            })
                            
                            print(f"✅ Successfully scraped and saved")
                    else:
                        print(f"⚠️ {message}")
                        results.append({
                            'court': court['text'],
                            'date': date_str,
                            'case_type': case_type,
                            'status': 'no_cases',
                            'message': message
                        })
                    
                    if idx < len(selected_courts):
                        self.go_back_to_search()
                        time.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Error processing court {court['text']}: {e}")
                    results.append({
                        'court': court['text'],
                        'date': date_str,
                        'case_type': case_type,
                        'status': 'error',
                        'error': str(e)
                    })
                    
                    self.go_back_to_search()
            
            print(f"\n{'='*60}")
            print(f"✅ Completed scraping {len(selected_courts)} court(s)")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ Fatal error in scraping: {e}")
        
        finally:
            self.close_driver()
        
        return results


if __name__ == "__main__":
    scraper = DelhiCourtsScraper(headless=False, browser="firefox")
    
    print("Testing with Firefox...")
    courts = scraper.fetch_available_courts()
    
    if courts:
        print(f"\n✅ SUCCESS! Found {len(courts)} courts")
        for court in courts[:3]:
            print(f"  - {court['text']}")
    else:
        print("\n❌ Failed to fetch courts")