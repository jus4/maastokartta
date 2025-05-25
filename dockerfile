# Use official Python 3 base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install build dependencies for some packages (like cffi, pyproj)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code into the container
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn to serve the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
