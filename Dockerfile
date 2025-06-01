FROM python:3.9-slim

# Install system dependencies, Firefox, and Mullvad VPN
RUN apt-get update && apt-get install -y \
    firefox-esr \
    curl \
    gnupg \
    wireguard \
    && rm -rf /var/lib/apt/lists/*

# Install Mullvad VPN
RUN curl -fsSL https://deb.mullvad.net/mullvad-keyring.asc | gpg --dearmor > /usr/share/keyrings/mullvad-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/mullvad-archive-keyring.gpg] https://deb.mullvad.net/stable/apt $(lsb_release -cs) main" > /etc/apt/sources.list.d/mullvad.list \
    && apt-get update \
    && apt-get install -y mullvad \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Make start script executable
RUN chmod +x /app/start.sh

# Run the start script
CMD ["/app/start.sh"]