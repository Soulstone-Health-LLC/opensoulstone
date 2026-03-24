# Dockerfile
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system packages (cached layer - changes rarely)
RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y --no-install-recommends \
  libpango-1.0-0 libpangoft2-1.0-0 \
  libffi-dev shared-mime-info && \
  rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app source (changes most frequently)
COPY . .

EXPOSE 8000
