FROM python:3.9-alpine

# Logs go straight to stream instead of being buffered
ENV PYTHONUNBUFFERED 1

# Copy Django app to container
WORKDIR /app
COPY . /app

# Install dependencies

## Python PostgreSQL client dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN ["pip", "install", "-r", "requirements.txt"]
## Removes temporary dependencies after Python dependencies are installed
RUN apk del .tmp-build-deps