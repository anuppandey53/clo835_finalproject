# Use an official Python base image for better compatibility and dependencies
FROM python:3.8-slim

# Set environment variables to reduce interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . /app

# Install system dependencies and Python packages
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        default-mysql-client \
        gcc \
        libssl-dev \
        libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 81 to allow access to the Flask application
EXPOSE 81

# Set the entry point for the container to run the Flask app
ENTRYPOINT ["python3", "app.py"]
