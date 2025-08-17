# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first for better Docker layer caching
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory
COPY backend/ ./

# Expose port 5000
EXPOSE 5000

# Force cache bust - Railway deployment v2.5.0
ENV DEPLOYMENT_VERSION=2.5.0
ENV CACHE_BUST=20250117_2024

# Start the Flask application
CMD ["python", "app.py"]
