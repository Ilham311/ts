FROM python:3.10-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask requests

# Install webcrack globally using npm
RUN npm install -g webcrack

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "script.py"]
