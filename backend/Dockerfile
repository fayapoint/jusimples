FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install dependencies first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend source code
COPY . /app

EXPOSE 5000

# Cache bust/version markers for Railway
ENV DEPLOYMENT_VERSION=2.5.2
ENV CACHE_BUST=20250817_1746

# Start the Flask application
CMD ["python", "app.py"]
