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
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    RECIPIENT_PHONE_NUMBER,
    STEAM_DECK_URL,
    STEAM_DECK_VERSIONS,
    CHECK_INTERVAL_SECONDS
)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

browser_options = Options()
browser_options.add_argument("--headless")
browser_options.set_preference("intl.accept_languages", "en-US,en")
# Add language parameter to URL if it doesn't already exist
url = STEAM_DECK_URL if "?l=english" in STEAM_DECK_URL else f"{STEAM_DECK_URL}?l=english"

def start():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=browser_options)
    driver.get(url)
    return driver


def refresh(driver):
    driver.refresh()
    # Wait for the page to load after refresh
    time.sleep(5)


def quit(driver):
    driver.quit()


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
        print(f"Current country: {country}")
        
        available_versions = []
        
        # Check each Steam Deck version
        for version in STEAM_DECK_VERSIONS:
            try:
                stock_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, version["xpath"]))
                )
                x = stock_element.text.strip()
                print(f"Found text for {version['name']}: {x}")
                
                if "Out of stock" not in x:
                    available_versions.append(version["name"])
            except Exception as e:
                print(f"Error checking {version['name']}: {str(e)}")
                continue
        
        if available_versions:
            message = f"The following Steam Deck versions are in stock: {', '.join(available_versions)} {STEAM_DECK_URL}"
            # Uncomment/comment to enable/disable SMS notifications
            client.messages.create(
                to=RECIPIENT_PHONE_NUMBER,
                from_=TWILIO_PHONE_NUMBER,
                body=message
            )
            print(message)
            status = 1
        else:
            print("All versions are out of stock")
            print("Time checked:", datetime.now())
            status = 0
            
        return status
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 0


def get_my_deck():
    c = 0
    driver = start()
    print("Starting driver...")
    time.sleep(10) ## DO NOT EDIT
    print("Starting scraper...")
    while True:
        try:
            if c < 11:
                status = runner(driver)
                if status == 1:
                    break
                time.sleep(CHECK_INTERVAL_SECONDS)  # Using config value for check interval
                c = c + 1
                refresh(driver)
            else:
                print("Rebooting")
                quit(driver)
                time.sleep(20) ## DO NOT EDIT
                c = 0
                driver = start()
        except Exception as e:
            print(f"Main loop error: {str(e)}")
            driver.quit()
            time.sleep(20) ## DO NOT EDIT
            get_my_deck()


get_my_deck()
