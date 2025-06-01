from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")
STEAM_DECK_URL = os.getenv("STEAM_DECK_URL")

# How often to check for Steam Deck availability (in seconds)
CHECK_INTERVAL_SECONDS = 60

# Steam Deck versions to monitor
STEAM_DECK_VERSIONS = [
    {
        "name": "Steam Deck 512 GB OLED",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '512 GB OLED')]/following::div[contains(@class, 'CartBtn')]/span"
    },
    {
        "name": "Steam Deck 1TB OLED",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '1TB OLED')]/following::div[contains(@class, 'CartBtn')]/span"
    },
    {
        "name": "Steam Deck 64 GB LCD",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '64 GB LCD')]/following::div[contains(@class, 'CartBtn')]/span"
    },
    {
        "name": "Steam Deck 256 GB LCD",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '256 GB LCD')]/following::div[contains(@class, 'CartBtn')]/span"
    },
    {
        "name": "Steam Deck 512 GB LCD",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '512 GB LCD')]/following::div[contains(@class, 'CartBtn')]/span"
    }
] 