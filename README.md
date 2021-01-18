# Backend Assessment

Backend challenge for interview process of the Junior Backend Dev position at T10.

## Instructions

The instructions for the challenge can be found [here](Instructions.md).

## The solution

The solution leverages Python, Django and the Django Rest Framework to create an API that satisfies the user's use cases. PostgreSQL is the choice for the DMBS.

And, finally, the solution runs in containers using Docker. Docker Compose is used for the container orchestration.

## How to run the project?

To run the project you'll need Docker and Docker Compose installed in your host machine (instructions here: [Docker](https://docs.docker.com/get-docker/), [Docker Compose](https://docs.docker.com/compose/install/)).

After cloning the repository, you need to run the following command

```bash
docker-compose up
```

Since it's the first run, Docker will download and prepare all the images and containers.

After everything is finished and you see Django message directing you to the localhost URL, you'll be ready to go.

The default port used is port 8000, but you can change it in the `docker-compose.yml` file if it's occupied.

## Important remarks

The project is set up in a way where the first run creates a superuser to facilitate testing. 

Those are the credentials:

```
User: root
Password: root
```

More details about credentials and other secrets can be found in the `.env` file (only in the repo because it's an assessment).

## API Endpoints

The root of the API is located in `http://localhost:8000/api/v1/`. The following endpoints are appended to that URL.

### Authentication (JWT)

#### /token/
Get an "access" and a "refresh" token to make requests with.

Request
```http
POST http://localhost:8000/api/v1/token/
```

```json
{
    "username": "root",
    "password": "root"
}
```

Response
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMTA3NzI2NSwianRpIjoiYjZlNTAwOGFhMmEyNGI0YTg1ODQ1ZGIyNDYyMTA0NTYiLCJ1c2VyX2lkIjoxfQ.rZnVL7nO1EC9t3AuRq49cMRqdpq0Czi-X_IJACx3_-0",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwOTkxNzY1LCJqdGkiOiJhN2FjNzNhYWY4N2E0ZmU1OTYyM2Y2OTMwMGZiYzQwMiIsInVzZXJfaWQiOjF9.waGh8eltC_5B2n463HBQiMGjljdNmWbDEoxVYIajaQ8"
}
```

#### /token/refresh/
Uses your "refresh" token to generate a new "access" one.

Request
```http
POST http://localhost:8000/api/v1/token/refresh/
```

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMTA3NzI2NSwianRpIjoiYjZlNTAwOGFhMmEyNGI0YTg1ODQ1ZGIyNDYyMTA0NTYiLCJ1c2VyX2lkIjoxfQ.rZnVL7nO1EC9t3AuRq49cMRqdpq0Czi-X_IJACx3_-0"
}
```

Response
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwOTkyMTUwLCJqdGkiOiI5OTRkZGFiZmNlNzM0Njk2OWQzYjE0N2VhMGQzZTY1YiIsInVzZXJfaWQiOjF9.QcjZF7akrOYTM0reSBYpzf9jvbdcv60K7-3N0qcBWqs"
}
```

### Reminder!

You'll need the `Authorization` header with `Bearer <access_token>` to request the following endpoints.

### Regular user endpoints

Endpoints any user can call. 

#### GET /products/
Requests the list of products created by the current user (or every product if the user is a superuser).

Request
```http
GET http://localhost:8000/api/v1/products/
```

Response
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Example Product",
            "notification_email": "example@example.com",
            "activation_issued": false,
            "activation_approved": null
        }
    ]
}
```

#### POST /products/
Allows the user to create a new product.

Request
```http
POST http://localhost:8000/api/v1/products/
```

```json
{
    "title": "Example Product 2",
    "notification_email": "newexample@example.com"
}
```

Response
```json
{
    "id": 2,
    "title": "Example Product 2",
    "notification_email": "newexample@example.com",
    "activation_issued": false,
    "activation_approved": null
}
```