# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and convert requirements from UTF-16 to UTF-8
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    # Convert requirements file encoding
    && iconv -f utf-16 -t utf-8 requirements.txt > requirements.utf8.txt \
    && mv requirements.utf8.txt requirements.txt

# Copy and install Python dependencies
COPY nomad-bot-main/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY nomad-bot-main/ .

# Copy .env if you prefer baked-in environment variables (optional)
# COPY .env ./

# Expose port if your bot serves webhooks (optional)
# EXPOSE 8443

# Define default command
CMD ["python", "main.py"]
