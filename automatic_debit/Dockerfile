FROM python:3.9-alpine

# Logs go straight to stream instead of being buffered
ENV PYTHONUNBUFFERED 1

# Copy Django app to container
WORKDIR /app
COPY . /app

# Install dependencies
RUN ["pip", "install", "-r", "requirements.txt"]