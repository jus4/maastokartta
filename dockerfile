FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps for pyproj and building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    proj-bin \
    libproj-dev \
    proj-data \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose your app port
EXPOSE 8000

# Command to run your app (adjust accordingly)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
