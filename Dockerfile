# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Step 3: Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y \
    nginx gcc build-essential libpcre3-dev git \
    pkg-config libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Create a directory for the application
WORKDIR /app

# Step 5: Copy the application files
COPY . /app/

# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Install uWSGI
#RUN pip install gunicorn

# Step 8: Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf


# Step 10: Expose the ports
EXPOSE 80

# Step 12: Start the application
CMD fastapi run application.py --port 8000 & \
     sleep 15 && \
     nginx -g "daemon off;"
