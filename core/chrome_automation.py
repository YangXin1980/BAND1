import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.logger import logger
from utils.helpers import find_chrome_executable

class ChromeAutomation:
    """Selenium WebDriver for Chrome automation and auto-login"""
    
    BAND_LOGIN_URL = "https://www.band.us/about/kr/intro"
    BAND_MAIN_URL = "https://www.band.us"
    
    def __init__(self, profile_dir=None):
        self.profile_dir = profile_dir
        self.driver = None
        self.chrome_exe = find_chrome_executable()
        
        if not self.chrome_exe:
            raise RuntimeError("Chrome not found. Please install Google Chrome.")
    
    def _create_chrome_options(self, user_data_dir=None):
        """Create Chrome options with settings"""
        options = Options()
        
        # User data directory for profile isolation
        if user_data_dir:
            options.add_argument(f"user-data-dir={user_data_dir}")
        
        # Preserve Google Translate feature
        options.add_argument("--enable-translate")
        options.add_argument("--enable-features=TranslateUI")
        
        # Performance optimization
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Additional settings
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        return options
    
    def create_driver(self, user_data_dir=None):
        """Create WebDriver instance"""
        try:
            options = self._create_chrome_options(user_data_dir)
            self.driver = webdriver.Chrome(
                executable_path=self.chrome_exe,
                options=options,
                service_log_path=None
            )
            logger.info("Chrome WebDriver created successfully")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to create WebDriver: {e}")
            raise
    
    def close(self):
        """Close WebDriver"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logger.info("WebDriver closed")
        except Exception as e:
            logger.error(f"Error closing WebDriver: {e}")
    
    def navigate_to(self, url, timeout=10):
        """Navigate to URL"""
        try:
            self.driver.get(url)
            logger.info(f"Navigated to {url}")
            time.sleep(2)  # Wait for page load
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    def login(self, email, password, timeout=30):
        """Auto-login to BAND"""
        try:
            logger.info(f"Starting login for {email}")
            
            # Navigate to login page
            self.navigate_to(self.BAND_LOGIN_URL)
            
            # Find email input field
            email_input = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email'] | //input[@type='text' and @placeholder*='email' or @placeholder*='Email']"))
            )
            email_input.clear()
            email_input.send_keys(email)
            logger.debug(f"Entered email: {email}")
            
            time.sleep(1)
            
            # Find password input field
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys(password)
            logger.debug("Entered password")
            
            time.sleep(1)
            
            # Click login button
            login_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(text(), 'Login') or contains(text(), 'Sign in') or contains(text(), '로그인')]"
            )
            login_button.click()
            logger.info("Clicked login button")
            
            # Wait for login to complete
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='band-main'] | //div[@class='main-content']"))
            )
            
            logger.info(f"Successfully logged in as {email}")
            return True
        except Exception as e:
            logger.error(f"Login failed for {email}: {e}")
            return False
    
    def wait_for_element(self, xpath, timeout=10):
        """Wait for element to appear"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            logger.error(f"Element not found: {xpath}")
            return None
    
    def execute_script(self, script, *args):
        """Execute JavaScript"""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"Script execution failed: {e}")
            return None
    
    def get_window_handle(self):
        """Get current window handle"""
        try:
            return self.driver.current_window_handle
        except Exception as e:
            logger.error(f"Failed to get window handle: {e}")
            return None
