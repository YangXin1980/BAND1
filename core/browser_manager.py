import os
import time
import subprocess
from threading import Thread
from pathlib import Path
from core.chrome_automation import ChromeAutomation
from core.account_storage import account_storage
from core.window_manager import window_manager
from utils.logger import logger
from utils.helpers import get_data_dir

class BrowserManager:
    """Manage multiple Chrome instances for BAND accounts"""
    
    def __init__(self):
        self.browsers = {}  # Store browser instances
        self.processes = {}  # Store process handles
        self.profiles_dir = os.path.join(get_data_dir(), 'chrome_profiles')
        os.makedirs(self.profiles_dir, exist_ok=True)
    
    def launch_browser_for_account(self, account_id, email, password):
        """Launch browser with auto-login for specific account"""
        try:
            logger.info(f"Launching browser for account {account_id}")
            
            # Create unique profile directory for this account
            profile_dir = os.path.join(self.profiles_dir, f"profile_{account_id}")
            os.makedirs(profile_dir, exist_ok=True)
            
            # Create and initialize Chrome automation
            chrome_auto = ChromeAutomation(profile_dir=profile_dir)
            driver = chrome_auto.create_driver(user_data_dir=profile_dir)
            
            # Store browser instance
            self.browsers[account_id] = {
                'driver': driver,
                'email': email,
                'account_id': account_id,
                'process': None,
                'window_handle': None
            }
            
            # Get window handle
            window_handle = chrome_auto.get_window_handle()
            self.browsers[account_id]['window_handle'] = window_handle
            
            # Attempt auto-login
            login_success = chrome_auto.login(email, password)
            
            if login_success:
                logger.info(f"Browser launched successfully for {email}")
                return True, "Browser launched successfully"
            else:
                logger.warning(f"Auto-login failed for {email}, manual login required")
                return True, "Browser launched, manual login required"
        
        except Exception as e:
            logger.error(f"Failed to launch browser for account {account_id}: {e}")
            return False, str(e)
    
    def launch_multiple_browsers(self, account_ids):
        """Launch browsers for multiple accounts"""
        results = []
        
        for account_id in account_ids:
            account = account_storage.get_account_with_password(account_id)
            if account:
                success, message = self.launch_browser_for_account(
                    account['id'],
                    account['email'],
                    account['password']
                )
                results.append({
                    'account_id': account_id,
                    'email': account['email'],
                    'success': success,
                    'message': message
                })
            else:
                results.append({
                    'account_id': account_id,
                    'success': False,
                    'message': 'Account not found'
                })
        
        # Arrange windows if enabled
        if len([r for r in results if r['success']]) > 0:
            self.arrange_windows(len([r for r in results if r['success']]))
        
        return results
    
    def arrange_windows(self, window_count):
        """Arrange launched browser windows automatically"""
        try:
            positions = window_manager.calculate_window_positions(window_count)
            
            browser_list = list(self.browsers.values())[:window_count]
            for i, browser in enumerate(browser_list):
                if i < len(positions):
                    try:
                        # Move window using driver
                        driver = browser['driver']
                        pos = positions[i]
                        driver.set_window_position(pos['x'], pos['y'])
                        driver.set_window_size(pos['width'], pos['height'])
                        logger.info(f"Arranged window for account {browser['account_id']}")
                    except Exception as e:
                        logger.warning(f"Failed to arrange window: {e}")
        except Exception as e:
            logger.error(f"Failed to arrange windows: {e}")
    
    def close_browser(self, account_id):
        """Close browser for specific account"""
        try:
            if account_id in self.browsers:
                browser_info = self.browsers[account_id]
                driver = browser_info['driver']
                driver.quit()
                del self.browsers[account_id]
                logger.info(f"Browser closed for account {account_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to close browser for account {account_id}: {e}")
            return False
    
    def close_all_browsers(self):
        """Close all open browsers"""
        try:
            account_ids = list(self.browsers.keys())
            for account_id in account_ids:
                self.close_browser(account_id)
            logger.info("All browsers closed")
            return True
        except Exception as e:
            logger.error(f"Failed to close all browsers: {e}")
            return False
    
    def get_browser_status(self):
        """Get status of all open browsers"""
        status = []
        for account_id, browser_info in self.browsers.items():
            try:
                # Check if driver still valid
                _ = browser_info['driver'].current_url
                status.append({
                    'account_id': account_id,
                    'email': browser_info['email'],
                    'status': 'running',
                    'url': browser_info['driver'].current_url
                })
            except Exception:
                status.append({
                    'account_id': account_id,
                    'email': browser_info['email'],
                    'status': 'closed'
                })
        return status
    
    def switch_to_account(self, account_id):
        """Switch focus to specific account's browser"""
        try:
            if account_id in self.browsers:
                browser_info = self.browsers[account_id]
                driver = browser_info['driver']
                driver.switch_to.window(driver.current_window_handle)
                logger.info(f"Switched to account {account_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to switch to account {account_id}: {e}")
            return False

# Global browser manager instance
browser_manager = BrowserManager()
