FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install dependencies with trusted hosts to handle SSL issues
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Install additional dependencies for genomic analysis
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org \
    streamlit \
    plotly \
    psycopg2-binary \
    google-cloud-pubsub

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/reports

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]