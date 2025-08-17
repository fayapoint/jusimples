# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the entire project first
COPY . .

# Install Python dependencies from backend directory
RUN pip install --no-cache-dir -r backend/requirements.txt

# Set working directory to backend
WORKDIR /app/backend

# Expose port 5000
EXPOSE 5000

# Force cache bust - Railway deployment v2.4.0
ENV DEPLOYMENT_VERSION=2.4.0
ENV CACHE_BUST=20250117_2003

# Start the Flask application
CMD ["python", "app.py"]
