FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Firefox and its dependencies
    firefox-esr \
    # Required for Firefox and Selenium
    xvfb \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libasound2 \
    # Required for downloading GeckoDriver
    wget \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install GeckoDriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.33.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.33.0-linux64.tar.gz

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    PATH="/usr/local/bin:${PATH}"

# Make start script executable
RUN chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]