# Steam Deck Stock Checker

A Python script that monitors the availability of Steam Deck devices on the Steam store and sends notifications when they become available.
Perfect for running on a cloud service like GCP or AWS.

## Features

- Monitors multiple Steam Deck versions simultaneously
- Supports both LCD and OLED models
- Configurable monitoring of specific versions
- SMS notifications via Twilio when stock becomes available
- Automatic retry mechanism with error handling
- Country-specific availability checking using VPN

## Supported Steam Deck Versions

The script can monitor the following Steam Deck versions:
- Steam Deck 512 GB OLED
- Steam Deck 1TB OLED
- Steam Deck 64 GB LCD
- Steam Deck 256 GB LCD
- Steam Deck 512 GB LCD

## Setup

### Prerequisites:
1. Create a free Twilio account. <small>(if you want SMS notification, see below for disabling this)</small>

### Option 1: Local Setup (no Docker)

1. Make sure you have Python 3. Most systems have it out of the box. Check with `python --version`. You will also need Firefox or Chrome installed. See below for switching.
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```
4. Create a `.env` file with your credentials (copy from `.env.example`)
5. Configure your Steam Deck versions in `config.py`
6. Run by typing in the terminal: `python .\get_my_deck.py`

### Option 2: Docker Setup (Recommended)

1. Install Docker and Docker Compose on your system
2. Create a `.env` file with your credentials (copy from `.env.example`)
3. Configure your Steam Deck versions in `config.py`
4. Build and run the container: <small>(note: in some cases the command might be `docker compose` instead of `docker-compose`, depends on system and how docker was installed)</small>
```bash
# Build & start the container
docker-compose up -d --build

# View logs in real-time
docker-compose logs -f

# Stop the container
docker-compose down
```

The Docker setup includes:
- Automatic container restart unless explicitly stopped
- Log rotation (10MB max size, 3 files)
- Timezone configuration
- Volume mounting for easy code updates
- Firefox browser pre-installed

## Configuration

You have two options for configuring your credentials and settings:

### 1. Simple (Beginner): Edit `config.py` Directly

Open `config.py` and fill in your details:
```python
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_number"
RECIPIENT_PHONE_NUMBER = "your_phone_number"
STEAM_DECK_URL = "https://store.steampowered.com/sale/steamdeckrefurbished"
```

### 2. Recommended (Secure & good practice): Use a `.env` File

1. Create a file named `.env` in your project root with the following structure:
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   RECIPIENT_PHONE_NUMBER=+1234567890
   STEAM_DECK_URL=https://store.steampowered.com/sale/steamdeckrefurbished
   ```
2. The script will automatically load these values. **Do not share your `.env` file or commit it to public repositories.**

### 3. Configure Steam Deck Versions to Monitor

Modify the `STEAM_DECK_VERSIONS` list in `config.py` to include only the versions you want to monitor. For example, to monitor only OLED models:

```python
STEAM_DECK_VERSIONS = [
    {
        "name": "Steam Deck 512 GB OLED",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '512 GB OLED')]/following::div[contains(@class, 'CartBtn')]/span"
    },
    {
        "name": "Steam Deck 1TB OLED",
        "xpath": "//div[contains(@class, '_1e4No10_bpJEyqWGdzhAs9')][contains(text(), '1TB OLED')]/following::div[contains(@class, 'CartBtn')]/span"
    }
]
```

## Switching Between Chrome and Firefox

The script can use either Chrome or Firefox as the web driver. By default, it is configured to use Firefox. To switch between them:

> **NOTE:** On the `deploy` branch this is not applicable. Firefox is integrated at a deeper level, installed by the docker setup. Switch at your own discretion. 

### For Chrome:
1. Install Chrome browser if you haven't already
2. Modify `get_my_deck.py` to use Chrome imports and driver:
```python
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# In the start() function:
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=browser_options)
```

### For Firefox:
1. Install Firefox browser if you haven't already
2. Use the current Firefox configuration in `get_my_deck.py`:
```python
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# In the start() function:
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=browser_options)
```

## Customization

### Notification Settings
- To enable/disable SMS notifications, edit the `runner` function in `get_my_deck.py`
- Comment/uncomment the `client.messages.create()` section to toggle notifications

## Error Handling

The script includes robust error handling:
- Automatically retries if a check fails
- Reboots the browser session periodically
- Provides detailed error messages in the console
- Continues monitoring even if one version check fails

### Deploying to Cloud Services
This app is perfect to be deployed as a cloud service. For free options, I recommend Google Cloud Platform (GCP).
This is not a tutorial on how to use a cloud service.
Check out the `deploy` branch.

## Features reserved for deployed version:
1. VPN Support trough any provider that offers Wireguard config. (`Mullvad`, NordVPN, ProtonVPN etc...) SD stocks very by country/region, if you need to set that, you can use this. Check out `docker-compose.yml` to switch between providers if something is not working.
2. Access real time logs anywhere trough 8080 port. Make sure to open that if you want this feature. For GCP:
`gcloud compute --project=[PROJECT_ID] firewall-rules create rule-for-deck-checker --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8080 --source-ranges=0.0.0.0/0`
