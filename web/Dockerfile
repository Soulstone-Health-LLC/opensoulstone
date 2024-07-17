# Dockerfile
FROM python:3.12

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy app files
COPY . /app

# System packages installation
RUN apt update && apt upgrade -y
RUN apt install wkhtmltopdf -y
