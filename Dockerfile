# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the entire project first
COPY . .

# Install dependencies from backend directory
RUN pip install --no-cache-dir -r backend/requirements.txt

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "app.py"]
