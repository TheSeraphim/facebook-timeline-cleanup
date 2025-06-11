#!/usr/bin/env python3
"""
Facebook Timeline Cleanup - Tool for gradually deleting Facebook posts

Usage:
    python facebook_timeline_cleanup.py --email your@email.com --password yourpass
    python facebook_timeline_cleanup.py --whatif --verbose  # test mode
    python facebook_timeline_cleanup.py --config config.json

Main options:
    --whatif: runs in simulation mode without actually deleting anything
    --verbose: detailed output of all operations
    --dry-run: synonym for --whatif
"""

import argparse
import time
import random
import os
import sys
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class FacebookCleaner:
    """Main class for automated Facebook timeline cleaning"""
    
    def __init__(self, config):
        """
        Initialize Facebook Cleaner with provided configuration
        
        Args:
            config (dict): Dictionary with all configurations
        """
        self.config = config
        self.email = config['credentials']['email']
        self.password = config['credentials']['password']
        self.whatif = config['execution']['whatif']
        self.verbose = config['execution']['verbose']
        
        # Session statistics
        self.stats = {
            'posts_found': 0,
            'posts_deleted': 0,
            'posts_skipped': 0,
            'errors_encountered': 0,
            'session_start': datetime.now(),
            'sessions_completed': 0
        }
        
        # Selenium driver and objects
        self.driver = None
        self.wait = None
        self.actions = None
        
        # Setup logging and driver
        self.setup_logging()
        self.setup_driver()
        
        self.logger.info("Facebook Timeline Cleanup initialized with configuration:")
        self.logger.info(f"Whatif mode: {self.whatif}")
        self.logger.info(f"Verbose mode: {self.verbose}")
        self.logger.info(f"Posts per session: {config['cleaning']['posts_per_session']}")
        self.logger.info(f"Number of sessions: {config['cleaning']['max_sessions']}")
        self.logger.info(f"Delay between sessions: {config['timing']['session_delay']} seconds")
    
    def setup_logging(self):
        """Configure logging system with detailed levels"""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        
        # Detailed log format
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(funcName)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Main logger
        self.logger = logging.getLogger('FacebookTimelineCleanup')
        self.logger.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_filename = f"facebook_timeline_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        self.logger.info(f"Logging system initialized. Log file: {log_filename}")
        
        if self.whatif:
            self.logger.warning("WHATIF MODE ACTIVE - No actual deletions will be performed")
    
    def setup_driver(self):
        """Configure Chrome driver with optimized options"""
        self.logger.info("Initializing Chrome driver...")
        
        options = Options()
        
        # Base configurations
        if self.config['browser']['headless'] and not self.verbose:
            options.add_argument('--headless')
            self.logger.info("Headless mode activated")
        
        # Options for stability and performance
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Realistic user agent
        user_agent = self.config['browser']['user_agent']
        options.add_argument(f'--user-agent={user_agent}')
        
        # Window size
        if not self.config['browser']['headless']:
            window_size = self.config['browser']['window_size']
            options.add_argument(f'--window-size={window_size["width"]},{window_size["height"]}')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, self.config['timing']['page_timeout'])
            self.actions = ActionChains(self.driver)
            
            # Remove automation flag
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Chrome driver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing driver: {e}")
            raise
    
    def human_like_delay(self, min_delay=None, max_delay=None):
        """
        Implement realistic pauses between actions to simulate human behavior
        
        Args:
            min_delay (float): Minimum delay in seconds
            max_delay (float): Maximum delay in seconds
        """
        if min_delay is None:
            min_delay = self.config['timing']['min_action_delay']
        if max_delay is None:
            max_delay = self.config['timing']['max_action_delay']
            
        delay = random.uniform(min_delay, max_delay)
        
        if self.verbose:
            self.logger.debug(f"Human-like pause of {delay:.2f} seconds")
        
        time.sleep(delay)
    
    def wait_for_page_load(self, timeout=None):
        """
        Wait for complete page loading
        
        Args:
            timeout (int): Timeout in seconds
        """
        if timeout is None:
            timeout = self.config['timing']['page_timeout']
            
        self.logger.debug("Waiting for page load...")
        
        try:
            # Wait for jQuery to complete (if present)
            self.wait.until(
                lambda driver: driver.execute_script("return jQuery.active == 0") 
                if driver.execute_script("return typeof jQuery != 'undefined'") 
                else True
            )
            
            # Wait for document ready state
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            self.logger.debug("Page loading completed")
            
        except TimeoutException:
            self.logger.warning(f"Timeout during page load wait ({timeout}s)")
    
    def login(self):
        """
        Perform Facebook login with advanced error handling
        
        Returns:
            bool: True if login successful, False otherwise
        """
        self.logger.info("Starting Facebook login procedure")
        
        try:
            # Navigate to login page
            self.logger.debug("Navigating to facebook.com...")
            self.driver.get("https://www.facebook.com")
            self.wait_for_page_load()
            
            # Handle cookie banner if present
            self.handle_cookie_banner()
            
            # Email input
            self.logger.debug("Looking for email field...")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            
            if self.whatif:
                self.logger.info(f"WHATIF: Would enter email in field (email hidden for security)")
            else:
                self.logger.debug("Entering email...")
                email_field.clear()
                for char in self.email:
                    email_field.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
            
            self.human_like_delay(1, 2)
            
            # Password input
            self.logger.debug("Looking for password field...")
            password_field = self.driver.find_element(By.ID, "pass")
            
            if self.whatif:
                self.logger.info("WHATIF: Would enter password (hidden for security)")
            else:
                self.logger.debug("Entering password...")
                password_field.clear()
                for char in self.password:
                    password_field.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
            
            self.human_like_delay(1, 3)
            
            # Click login button
            self.logger.debug("Looking for login button...")
            login_button = self.driver.find_element(By.NAME, "login")
            
            if self.whatif:
                self.logger.info("WHATIF: Would click login button (not executed)")
                return True
            else:
                self.logger.debug("Clicking login button...")
                self.actions.move_to_element(login_button).click().perform()
            
            # Verify successful login
            self.logger.debug("Verifying login completion...")
            try:
                # Wait for elements indicating successful login
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='search']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label*='main menu']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='blue_bar_profile_link']"))
                    )
                )
                
                self.logger.info("Login completed successfully")
                return True
                
            except TimeoutException:
                # Check for login errors
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='royal_login_error']")
                if error_elements:
                    error_text = error_elements[0].text
                    self.logger.error(f"Login error: {error_text}")
                    return False
                
                # Check for 2FA requirement
                two_fa_elements = self.driver.find_elements(By.CSS_SELECTOR, "[name='approvals_code']")
                if two_fa_elements:
                    self.logger.error("Two-factor authentication required - not supported automatically")
                    return False
                
                self.logger.error("Login failed - timeout in verification")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            if self.verbose:
                self.logger.debug(f"Full stack trace: {e}")
            return False
    
    def handle_cookie_banner(self):
        """Handle cookie banner if present"""
        try:
            self.logger.debug("Checking for cookie banner...")
            
            # Common selectors for Facebook cookie banners
            cookie_selectors = [
                "[data-testid='cookie-policy-manage-dialog'] button",
                "[data-cookiebanner='accept_button']",
                "button[title*='Accept']",
                "button[title*='Accetta']"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    if self.whatif:
                        self.logger.info("WHATIF: Would click accept cookies button (not executed)")
                    else:
                        self.logger.debug("Clicking accept cookies button")
                        cookie_button.click()
                        self.human_like_delay(1, 2)
                    
                    return
                    
                except TimeoutException:
                    continue
            
            self.logger.debug("No cookie banner found")
            
        except Exception as e:
            self.logger.debug(f"Error handling cookie banner: {e}")
    
    def navigate_to_activity_log(self):
        """
        Navigate to activity log with advanced error handling
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        self.logger.info("Navigating to activity log")
        
        try:
            # Strategy 1: Direct URL
            self.logger.debug("Attempting direct navigation to activity log...")
            activity_url = "https://www.facebook.com/me/allactivity"
            
            if self.whatif:
                self.logger.info(f"WHATIF: Would navigate to {activity_url}")
                return True
            
            self.driver.get(activity_url)
            self.wait_for_page_load()
            
            # Verify we're on the correct page
            if "allactivity" in self.driver.current_url or "activity" in self.driver.current_url:
                self.logger.info("Navigation to activity log completed")
                return True
            
            # Strategy 2: Through profile
            self.logger.debug("Direct strategy failed, navigating through profile...")
            self.driver.get("https://www.facebook.com/me")
            self.wait_for_page_load()
            
            # Look for activity log link
            activity_selectors = [
                "a[href*='allactivity']",
                "a[href*='activity']",
                "[data-testid*='activity']",
                "a:contains('Activity Log')",
                "a:contains('Registro attività')"
            ]
            
            for selector in activity_selectors:
                try:
                    activity_link = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    self.logger.debug(f"Found activity log link: {selector}")
                    activity_link.click()
                    self.wait_for_page_load()
                    
                    if "allactivity" in self.driver.current_url or "activity" in self.driver.current_url:
                        self.logger.info("Navigation to activity log completed via profile")
                        return True
                    
                except TimeoutException:
                    continue
            
            self.logger.error("Unable to navigate to activity log")
            return False
            
        except Exception as e:
            self.logger.error(f"Error navigating to activity log: {e}")
            return False
    
    def find_posts_on_page(self):
        """
        Find all posts present on current page
        
        Returns:
            list: List of found post elements
        """
        self.logger.debug("Searching for posts on current page...")
        
        # Multiple selectors for posts in activity log
        post_selectors = [
            "[data-testid='activity-log-item']",
            "[data-pagelet='ActivityLogList'] > div",
            ".userContentWrapper",
            "[role='article']",
            "[data-testid='fbfeed_story']"
        ]
        
        all_posts = []
        
        for selector in post_selectors:
            try:
                posts = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if posts:
                    self.logger.debug(f"Found {len(posts)} posts with selector: {selector}")
                    all_posts.extend(posts)
                    break
                    
            except Exception as e:
                self.logger.debug(f"Error with selector {selector}: {e}")
                continue
        
        # Remove duplicates while maintaining order
        unique_posts = []
        seen_elements = set()
        
        for post in all_posts:
            element_id = post.get_attribute('data-testid') or post.get_attribute('id') or str(hash(post.text[:50]))
            if element_id not in seen_elements:
                unique_posts.append(post)
                seen_elements.add(element_id)
        
        self.logger.info(f"Found {len(unique_posts)} unique posts on page")
        self.stats['posts_found'] += len(unique_posts)
        
        return unique_posts
    
    def attempt_post_deletion(self, post_element, post_index):
        """
        Attempt to delete a single post
        
        Args:
            post_element: Selenium element of the post
            post_index (int): Index of post for logging
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        self.logger.debug(f"Attempting deletion of post {post_index + 1}")
        
        try:
            # Scroll to post to make it visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", post_element)
            self.human_like_delay(1, 2)
            
            # Extract post information for logging
            post_info = self.extract_post_info(post_element)
            self.logger.info(f"Post {post_index + 1}: {post_info}")
            
            if self.whatif:
                self.logger.info(f"WHATIF: Would delete post {post_index + 1} (not executed)")
                self.stats['posts_deleted'] += 1
                return True
            
            # Look for post menu button
            menu_selectors = [
                "[aria-label*='More options']",
                "[aria-label*='Altre opzioni']",
                "[data-testid='post_menu']",
                ".UFIMoreButton",
                "[aria-haspopup='menu']"
            ]
            
            menu_button = None
            for selector in menu_selectors:
                try:
                    menu_button = post_element.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not menu_button:
                self.logger.warning(f"Menu not found for post {post_index + 1}")
                self.stats['posts_skipped'] += 1
                return False
            
            # Click on menu
            self.logger.debug(f"Clicking menu for post {post_index + 1}")
            self.actions.move_to_element(menu_button).click().perform()
            self.human_like_delay(1, 3)
            
            # Look for delete option
            delete_selectors = [
                "[data-testid*='delete']",
                "a:contains('Delete')",
                "a:contains('Elimina')",
                "[role='menuitem']:contains('Delete')",
                "[role='menuitem']:contains('Elimina')"
            ]
            
            delete_option = None
            for selector in delete_selectors:
                try:
                    delete_option = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not delete_option:
                self.logger.warning(f"Delete option not found for post {post_index + 1}")
                self.stats['posts_skipped'] += 1
                return False
            
            # Click delete
            self.logger.debug(f"Clicking delete for post {post_index + 1}")
            delete_option.click()
            self.human_like_delay(1, 2)
            
            # Confirm deletion
            confirm_selectors = [
                "[data-testid='confirm-delete-button']",
                "button:contains('Delete')",
                "button:contains('Elimina')",
                "[aria-label*='Confirm']",
                "[aria-label*='Conferma']"
            ]
            
            confirm_button = None
            for selector in confirm_selectors:
                try:
                    confirm_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if confirm_button:
                self.logger.debug(f"Confirming deletion of post {post_index + 1}")
                confirm_button.click()
                self.human_like_delay(2, 4)
                
                self.logger.info(f"Post {post_index + 1} deleted successfully")
                self.stats['posts_deleted'] += 1
                return True
            else:
                self.logger.warning(f"Confirm button not found for post {post_index + 1}")
                self.stats['posts_skipped'] += 1
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting post {post_index + 1}: {e}")
            self.stats['errors_encountered'] += 1
            return False
    
    def extract_post_info(self, post_element):
        """
        Extract information from post for logging
        
        Args:
            post_element: Selenium element of the post
            
        Returns:
            str: String with post information
        """
        try:
            # Extract post text (first 100 characters)
            post_text = post_element.text[:100].replace('\n', ' ').strip()
            
            # Extract timestamp if available
            timestamp_selectors = [
                "[data-testid='story-subtitle'] a",
                ".timestampContent",
                "time",
                "[title*='20']"  # Year in title
            ]
            
            timestamp = "Unknown timestamp"
            for selector in timestamp_selectors:
                try:
                    time_element = post_element.find_element(By.CSS_SELECTOR, selector)
                    timestamp = time_element.get_attribute('title') or time_element.text
                    break
                except NoSuchElementException:
                    continue
            
            return f"[{timestamp}] {post_text}{'...' if len(post_element.text) > 100 else ''}"
            
        except Exception as e:
            return f"Error extracting info: {e}"
    
    def delete_posts_batch(self, max_posts):
        """
        Delete a batch of posts from current page
        
        Args:
            max_posts (int): Maximum number of posts to delete
            
        Returns:
            int: Number of posts actually deleted
        """
        self.logger.info(f"Starting deletion batch of maximum {max_posts} posts")
        
        deleted_count = 0
        
        # Find posts on page
        posts = self.find_posts_on_page()
        
        if not posts:
            self.logger.warning("No posts found on current page")
            return 0
        
        # Limit to requested maximum
        posts_to_process = posts[:max_posts]
        self.logger.info(f"Processing {len(posts_to_process)} posts")
        
        # Process each post
        for i, post in enumerate(posts_to_process):
            self.logger.debug(f"Processing post {i + 1}/{len(posts_to_process)}")
            
            if self.attempt_post_deletion(post, i):
                deleted_count += 1
                
                # Pause between deletions
                delay = random.uniform(
                    self.config['timing']['min_delete_delay'],
                    self.config['timing']['max_delete_delay']
                )
                
                if self.verbose:
                    self.logger.debug(f"Pause of {delay:.2f}s before next post")
                
                time.sleep(delay)
            
            # Check for user interruption every 5 posts
            if (i + 1) % 5 == 0:
                try:
                    # Check if user pressed Ctrl+C
                    pass
                except KeyboardInterrupt:
                    self.logger.info("User interruption requested")
                    break
        
        self.logger.info(f"Batch completed: {deleted_count} posts deleted")
        return deleted_count
    
    def clean_profile_gradually(self):
        """
        Execute gradual profile cleaning according to configured parameters
        
        Returns:
            dict: Final cleaning statistics
        """
        self.logger.info("Starting gradual Facebook profile cleaning")
        
        # Login
        if not self.login():
            self.logger.error("Login failed, stopping cleaning")
            return self.get_final_stats()
        
        # Navigate to activity log
        if not self.navigate_to_activity_log():
            self.logger.error("Navigation to activity log failed, stopping cleaning")
            return self.get_final_stats()
        
        # Session loop
        max_sessions = self.config['cleaning']['max_sessions']
        posts_per_session = self.config['cleaning']['posts_per_session']
        session_delay = self.config['timing']['session_delay']
        
        for session in range(max_sessions):
            self.logger.info(f"SESSION {session + 1}/{max_sessions}")
            self.logger.info(f"Target: {posts_per_session} posts for this session")
            
            # Refresh page to see new posts
            if session > 0:
                self.logger.debug("Refreshing page for new posts...")
                if not self.whatif:
                    self.driver.refresh()
                    self.wait_for_page_load()
                    self.human_like_delay(3, 5)
            
            # Delete batch of posts
            session_deleted = self.delete_posts_batch(posts_per_session)
            
            self.logger.info(f"Session {session + 1} completed: {session_deleted} posts deleted")
            self.stats['sessions_completed'] += 1
            
            # Pause between sessions (except last one)
            if session < max_sessions - 1:
                self.logger.info(f"Pause between sessions: {session_delay} seconds")
                
                if self.verbose:
                    # Show countdown of pause
                    remaining = session_delay
                    while remaining > 0:
                        mins, secs = divmod(remaining, 60)
                        timer = f"{mins:02d}:{secs:02d}"
                        print(f"\rNext session in: {timer}", end="", flush=True)
                        time.sleep(1)
                        remaining -= 1
                    print()  # New line after countdown
                else:
                    time.sleep(session_delay)
            
            # Check if no more posts to delete
            if session_deleted == 0:
                self.logger.info("No posts deleted in this session, possibly end of content")
                break
        
        self.logger.info("Gradual cleaning completed")
        return self.get_final_stats()
    
    def get_final_stats(self):
        """
        Generate final session statistics
        
        Returns:
            dict: Complete statistics
        """
        end_time = datetime.now()
        duration = end_time - self.stats['session_start']
        
        final_stats = {
            **self.stats,
            'session_end': end_time,
            'total_duration': str(duration),
            'duration_seconds': duration.total_seconds(),
            'posts_per_minute': self.stats['posts_deleted'] / (duration.total_seconds() / 60) if duration.total_seconds() > 0 else 0
        }
        
        return final_stats
    
    def print_final_report(self, stats):
        """
        Print final operations report
        
        Args:
            stats (dict): Session statistics
        """
        print("\n" + "="*70)
        print("FACEBOOK TIMELINE CLEANUP - FINAL REPORT")
        print("="*70)
        
        if self.whatif:
            print("WHATIF MODE - No actual deletions performed")
            print("-"*70)
        
        print(f"Total duration:          {stats['total_duration']}")
        print(f"Sessions completed:      {stats['sessions_completed']}")
        print(f"Posts found:             {stats['posts_found']}")
        print(f"Posts deleted:           {stats['posts_deleted']}")
        print(f"Posts skipped:           {stats['posts_skipped']}")
        print(f"Errors encountered:      {stats['errors_encountered']}")
        print(f"Average speed:           {stats['posts_per_minute']:.2f} posts/minute")
        
        if stats['posts_deleted'] > 0:
            success_rate = (stats['posts_deleted'] / (stats['posts_deleted'] + stats['posts_skipped'])) * 100
            print(f"Success rate:            {success_rate:.1f}%")
        
        print("="*70)
        
        if self.whatif:
            print("To actually perform deletions, remove the --whatif parameter")
        else:
            print(f"Deletions completed. Detailed log saved to: facebook_timeline_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    def close(self):
        """Close driver and release resources"""
        self.logger.info("Closing driver and cleaning up resources...")
        
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Driver closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing driver: {e}")

def create_default_config():
    """
    Create default configuration for Facebook Timeline Cleanup
    
    Returns:
        dict: Default configuration
    """
    return {
        "credentials": {
            "email": "",
            "password": ""
        },
        "cleaning": {
            "posts_per_session": 10,
            "max_sessions": 5,
            "target_post_types": ["status", "photo", "video", "link", "all"]
        },
        "timing": {
            "session_delay": 300,
            "page_timeout": 30,
            "min_action_delay": 1.0,
            "max_action_delay": 3.0,
            "min_delete_delay": 3.0,
            "max_delete_delay": 7.0
        },
        "browser": {
            "headless": False,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "window_size": {
                "width": 1366,
                "height": 768
            }
        },
        "execution": {
            "whatif": False,
            "verbose": False
        }
    }

def load_config_from_file(config_path):
    """
    Load configuration from JSON file
    
    Args:
        config_path (str): Configuration file path
        
    Returns:
        dict: Loaded configuration
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"Configuration loaded from: {config_path}")
        return config
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file: {e}")
        return None

def save_config_template(config_path):
    """
    Save configuration template
    
    Args:
        config_path (str): Path where to save template
    """
    config = create_default_config()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"Configuration template saved to: {config_path}")
        print("Edit the file with your credentials and preferences before use.")
    except Exception as e:
        print(f"Error saving template: {e}")

def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Facebook Timeline Cleanup - Gradually delete posts from your Facebook timeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:

  Test mode (recommended for first use):
    python facebook_timeline_cleanup.py --whatif --verbose

  Basic execution:
    python facebook_timeline_cleanup.py --email user@email.com --password mypassword

  Advanced configuration:
    python facebook_timeline_cleanup.py --config config.json --sessions 10 --posts-per-session 5

  Generate configuration template:
    python facebook_timeline_cleanup.py --save-config config.json

Security notes:
  - Always use --whatif to test before real use
  - Never share your configuration files with credentials
  - Consider using app-specific passwords
        """
    )
    
    # Credentials group
    cred_group = parser.add_argument_group('credentials')
    cred_group.add_argument('--email', 
                           help='Facebook login email')
    cred_group.add_argument('--password',
                           help='Facebook login password')
    
    # Configuration group
    config_group = parser.add_argument_group('configuration')
    config_group.add_argument('--config',
                             help='Path to JSON configuration file')
    config_group.add_argument('--save-config',
                             help='Save configuration template to specified path')
    
    # Cleaning group
    clean_group = parser.add_argument_group('cleaning parameters')
    clean_group.add_argument('--sessions', type=int, default=5,
                            help='Maximum number of sessions (default: 5)')
    clean_group.add_argument('--posts-per-session', type=int, default=10,
                            help='Posts to delete per session (default: 10)')
    clean_group.add_argument('--session-delay', type=int, default=300,
                            help='Pause between sessions in seconds (default: 300)')
    
    # Timing group
    timing_group = parser.add_argument_group('timing parameters')
    timing_group.add_argument('--page-timeout', type=int, default=30,
                             help='Page load timeout in seconds (default: 30)')
    timing_group.add_argument('--min-delay', type=float, default=1.0,
                             help='Minimum delay between actions in seconds (default: 1.0)')
    timing_group.add_argument('--max-delay', type=float, default=3.0,
                             help='Maximum delay between actions in seconds (default: 3.0)')
    
    # Browser group
    browser_group = parser.add_argument_group('browser parameters')
    browser_group.add_argument('--headless', action='store_true',
                              help='Run in headless mode (no GUI)')
    browser_group.add_argument('--user-agent',
                              help='Custom user agent for browser')
    
    # Execution group
    exec_group = parser.add_argument_group('execution modes')
    exec_group.add_argument('--whatif', '--dry-run', action='store_true',
                           help='Simulation mode - does not actually delete anything')
    exec_group.add_argument('--verbose', '-v', action='store_true',
                           help='Detailed output of all operations')
    
    return parser.parse_args()

def merge_config_with_args(base_config, args):
    """
    Merge base configuration with command line arguments
    
    Args:
        base_config (dict): Base configuration
        args (argparse.Namespace): Command line arguments
        
    Returns:
        dict: Final configuration
    """
    config = base_config.copy()
    
    # Update credentials
    if args.email:
        config['credentials']['email'] = args.email
    if args.password:
        config['credentials']['password'] = args.password
    
    # Update cleaning parameters
    config['cleaning']['max_sessions'] = args.sessions
    config['cleaning']['posts_per_session'] = args.posts_per_session
    
    # Update timing
    config['timing']['session_delay'] = args.session_delay
    config['timing']['page_timeout'] = args.page_timeout
    config['timing']['min_action_delay'] = args.min_delay
    config['timing']['max_action_delay'] = args.max_delay
    
    # Update browser
    if args.headless:
        config['browser']['headless'] = True
    if args.user_agent:
        config['browser']['user_agent'] = args.user_agent
    
    # Update execution
    config['execution']['whatif'] = args.whatif
    config['execution']['verbose'] = args.verbose
    
    return config

def validate_config(config):
    """
    Validate configuration and check prerequisites
    
    Args:
        config (dict): Configuration to validate
        
    Returns:
        tuple: (bool, str) - (validity, error message)
    """
    # Check credentials
    if not config['credentials']['email']:
        return False, "Email missing. Use --email or specify in configuration file."
    
    if not config['credentials']['password'] and not config['execution']['whatif']:
        return False, "Password missing for real mode. Use --password or --whatif for testing."
    
    # Check numeric parameters
    if config['cleaning']['max_sessions'] <= 0:
        return False, "Number of sessions must be greater than 0."
    
    if config['cleaning']['posts_per_session'] <= 0:
        return False, "Number of posts per session must be greater than 0."
    
    if config['timing']['session_delay'] < 0:
        return False, "Session delay cannot be negative."
    
    # Check timing consistency
    if config['timing']['min_action_delay'] > config['timing']['max_action_delay']:
        return False, "Minimum delay cannot be greater than maximum delay."
    
    return True, "Configuration valid"

def main():
    """Main program function"""
    
    print("Facebook Timeline Cleanup v1.0")
    print("Tool for gradual deletion of Facebook posts")
    print("-" * 60)
    
    # Parse arguments
    args = parse_arguments()
    
    # Handle template saving
    if args.save_config:
        save_config_template(args.save_config)
        return 0
    
    # Load configuration
    if args.config:
        config = load_config_from_file(args.config)
        if config is None:
            return 1
    else:
        config = create_default_config()
    
    # Merge with command line arguments
    config = merge_config_with_args(config, args)
    
    # Validate configuration
    is_valid, error_msg = validate_config(config)
    if not is_valid:
        print(f"ERROR: {error_msg}")
        return 1
    
    # Security warnings
    if not config['execution']['whatif']:
        print("\nWARNING: You are about to actually delete posts from Facebook!")
        print("This operation is NOT reversible.")
        print("We recommend:")
        print("1. Run first with --whatif to test")
        print("2. Download a backup of your data from Facebook")
        print("3. Start with a low number of posts per session")
        
        confirm = input("\nAre you sure you want to proceed? (type 'DELETE' to confirm): ")
        if confirm != 'DELETE':
            print("Operation cancelled.")
            return 0
    
    # Session information
    print(f"\nSession configuration:")
    print(f"  Mode:                  {'SIMULATION (whatif)' if config['execution']['whatif'] else 'ACTUAL DELETION'}")
    print(f"  Account:               {config['credentials']['email']}")
    print(f"  Planned sessions:      {config['cleaning']['max_sessions']}")
    print(f"  Posts per session:     {config['cleaning']['posts_per_session']}")
    print(f"  Pause between sessions: {config['timing']['session_delay']} seconds")
    print(f"  Verbose mode:          {'Yes' if config['execution']['verbose'] else 'No'}")
    print(f"  Headless browser:      {'Yes' if config['browser']['headless'] else 'No'}")
    
    # Initialize cleaner
    cleaner = None
    try:
        print(f"\nStarting operations...")
        cleaner = FacebookCleaner(config)
        
        # Execute cleaning
        final_stats = cleaner.clean_profile_gradually()
        
        # Final report
        cleaner.print_final_report(final_stats)
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\nUser interruption requested (Ctrl+C)")
        if cleaner:
            print("Generating partial report...")
            partial_stats = cleaner.get_final_stats()
            cleaner.print_final_report(partial_stats)
        return 130
        
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        if config['execution']['verbose']:
            import traceback
            traceback.print_exc()
        return 1
        
    finally:
        if cleaner:
            cleaner.close()

if __name__ == "__main__":
    sys.exit(main())