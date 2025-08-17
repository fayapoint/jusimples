# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt from backend directory to root for installation
COPY backend/requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set working directory to backend
WORKDIR /app/backend

# Expose port 5000
EXPOSE 5000

# Force cache bust - Railway deployment v2.4.0
ENV DEPLOYMENT_VERSION=2.4.0
ENV CACHE_BUST=20250117_2000

# Start the Flask application
CMD ["python", "app.py"]
