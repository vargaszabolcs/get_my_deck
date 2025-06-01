from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from twilio.rest import Client
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
import threading
from flask import Flask, jsonify
import os
import logging
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    RECIPIENT_PHONE_NUMBER,
    STEAM_DECK_URL,
    STEAM_DECK_VERSIONS,
    CHECK_INTERVAL_SECONDS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

browser_options = Options()
browser_options.add_argument("--headless")
browser_options.add_argument("--no-sandbox")
browser_options.add_argument("--disable-dev-shm-usage")
browser_options.set_preference("intl.accept_languages", "en-US,en")
# Add language parameter to URL if it doesn't already exist
url = STEAM_DECK_URL if "?l=english" in STEAM_DECK_URL else f"{STEAM_DECK_URL}?l=english"

def start():
    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=browser_options)
        driver.get(url)
        logger.info("Browser started successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to start browser: {str(e)}")
        raise

def refresh(driver):
    try:
        driver.refresh()
        # Wait for the page to load after refresh
        time.sleep(5)
        logger.info("Page refreshed successfully")
    except Exception as e:
        logger.error(f"Failed to refresh page: {str(e)}")
        raise

def quit(driver):
    try:
        driver.quit()
        logger.info("Browser closed successfully")
    except Exception as e:
        logger.error(f"Failed to close browser: {str(e)}")

def runner(driver):
    try:
        # Wait up to 10 seconds for the elements to be present
        wait = WebDriverWait(driver, 10)
        
        # Get country information
        config_element = wait.until(
            EC.presence_of_element_located((By.ID, "application_config"))
        )
        config_data = config_element.get_attribute("data-config")
        import json
        config = json.loads(config_data)
        country = config.get("COUNTRY", "Unknown")
        logger.info(f"Current country: {country}")
        
        available_versions = []
        
        # Check each Steam Deck version
        for version in STEAM_DECK_VERSIONS:
            try:
                stock_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, version["xpath"]))
                )
                x = stock_element.text.strip()
                logger.info(f"Found text for {version['name']}: {x}")
                
                if "Out of stock" not in x:
                    available_versions.append(version["name"])
            except Exception as e:
                logger.error(f"Error checking {version['name']}: {str(e)}")
                continue
        
        if available_versions:
            message = f"The following Steam Deck versions are in stock: {', '.join(available_versions)} {STEAM_DECK_URL}"
            # Uncomment/comment to enable/disable SMS notifications
            client.messages.create(
                to=RECIPIENT_PHONE_NUMBER,
                from_=TWILIO_PHONE_NUMBER,
                body=message
            )
            logger.info(message)
            status = 1
        else:
            logger.info("All versions are out of stock")
            logger.info(f"Time checked: {datetime.now()}")
            status = 0
            
        return status
    except Exception as e:
        logger.error(f"Error occurred in runner: {str(e)}")
        return 0

def monitor_steam_deck():
    logger.info("monitor_steam_deck function started")
    c = 0
    driver = None
    try:
        driver = start()
        logger.info("Starting driver...")
        time.sleep(10)  # DO NOT EDIT
        logger.info("Starting scraper...")
        while True:
            try:
                if c < 11:
                    logger.info(f"Starting check iteration {c+1}")
                    status = runner(driver)
                    if status == 1:
                        logger.info("Found available Steam Deck!")
                        break
                    logger.info(f"Check iteration {c+1} completed. Waiting {CHECK_INTERVAL_SECONDS} seconds before next check.")
                    time.sleep(CHECK_INTERVAL_SECONDS)  # Using config value for check interval
                    c = c + 1
                    refresh(driver)
                else:
                    logger.info("Rebooting after 11 iterations")
                    quit(driver)
                    time.sleep(20)  # DO NOT EDIT
                    c = 0
                    driver = start()
            except Exception as e:
                logger.error(f"Main loop error: {str(e)}")
                if driver:
                    quit(driver)
                time.sleep(20)  # DO NOT EDIT
                monitor_steam_deck()
    except Exception as e:
        logger.error(f"Fatal error in monitor_steam_deck: {str(e)}")
        if driver:
            quit(driver)

@app.route('/')
def home():
    return jsonify({"status": "Steam Deck Stock Checker is running"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    logger.info("Application starting up...")
    # Start the monitoring thread
    monitor_thread = threading.Thread(target=monitor_steam_deck, daemon=True)
    monitor_thread.start()
    logger.info("Monitoring thread started")
    
    # Start the Flask app
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
else:
    # When running with Gunicorn, just start the monitoring thread
    logger.info("Application starting up in production mode...")
    monitor_thread = threading.Thread(target=monitor_steam_deck, daemon=True)
    monitor_thread.start()
    logger.info("Monitoring thread started in production mode")
