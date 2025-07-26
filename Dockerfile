FROM python:3.9-slim

WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package*.json ./
COPY requirements.txt ./

# Install dependencies
RUN npm install
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 8000

# Start the server
CMD ["python3", "server.py"]