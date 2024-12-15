# Use python:3.11-slim as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for psycopg2 and netcat (for wait-for-it.sh)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \  
    && rm -rf /var/lib/apt/lists/*

# Update pip
RUN pip install --upgrade pip

# Copy the dependencies file to the container
COPY requirements.txt .

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY ./app /app/app

# Copy the wait-for-it.sh script into the container
COPY wait-for-it.sh /wait-for-it.sh

# Make sure the script is executable
RUN chmod +x /wait-for-it.sh

# Define PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app

# Expose port 8000 for the application
EXPOSE 8000

# Start the application after ensuring Kafka and the database are ready
CMD ["/wait-for-it.sh", "db:5432", "--", "/wait-for-it.sh", "kafka:9092", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
