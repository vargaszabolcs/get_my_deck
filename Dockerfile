FROM python:3.9-slim

# Install system dependencies and Firefox
RUN apt-get update && apt-get install -y \
    firefox-esr \
    curl \
    gnupg \
    wireguard \
    && rm -rf /var/lib/apt/lists/*

# Install Mullvad VPN using official repository
RUN curl -fsSLo /usr/share/keyrings/mullvad-keyring.asc https://repository.mullvad.net/deb/mullvad-keyring.asc \
    && echo "deb [signed-by=/usr/share/keyrings/mullvad-keyring.asc arch=$( dpkg --print-architecture )] https://repository.mullvad.net/deb/stable stable main" > /etc/apt/sources.list.d/mullvad.list \
    && apt-get update \
    && apt-get install -y mullvad-vpn \
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

# Create a script to start the VPN and then the application
RUN echo '#!/bin/bash\n\
mullvad account set ${MULLVAD_ACCOUNT}\n\
mullvad connect\n\
mullvad set location ro\n\
sleep 5\n\
gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 2 --worker-class gthread --timeout 0 get_my_deck:app\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the start script
CMD ["/app/start.sh"]