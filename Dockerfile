FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY . .

# Install Python packages
RUN pip install --no-cache-dir discord.py==2.3.2 requests==2.31.0

# Run the bot
CMD ["python", "bot_simple.py"]