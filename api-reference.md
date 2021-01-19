# API Reference

The root of the API is located in `http://localhost:8000/api/v1/`. The following endpoints are appended to that URL.

Many of those routes are paginated. This means the responses include a `count`, `next`, `previous` and a `results`. The page size is 5 entries.

## Authentication (JWT)

### POST /token/
Get an "access" and a "refresh" token to make requests with.

Request
```http
POST http://localhost:8000/api/v1/token/
```

```js
{
    "username": "root",
    "password": "root"
}
```

Response
```js
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMTA3NzI2NSwianRpIjoiYjZlNTAwOGFhMmEyNGI0YTg1ODQ1ZGIyNDYyMTA0NTYiLCJ1c2VyX2lkIjoxfQ.rZnVL7nO1EC9t3AuRq49cMRqdpq0Czi-X_IJACx3_-0",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwOTkxNzY1LCJqdGkiOiJhN2FjNzNhYWY4N2E0ZmU1OTYyM2Y2OTMwMGZiYzQwMiIsInVzZXJfaWQiOjF9.waGh8eltC_5B2n463HBQiMGjljdNmWbDEoxVYIajaQ8"
}
```

### POST /token/refresh/
Uses your "refresh" token to generate a new "access" one.

Request
```http
POST http://localhost:8000/api/v1/token/refresh/
```

```js
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMTA3NzI2NSwianRpIjoiYjZlNTAwOGFhMmEyNGI0YTg1ODQ1ZGIyNDYyMTA0NTYiLCJ1c2VyX2lkIjoxfQ.rZnVL7nO1EC9t3AuRq49cMRqdpq0Czi-X_IJACx3_-0"
}
```

Response
```js
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwOTkyMTUwLCJqdGkiOiI5OTRkZGFiZmNlNzM0Njk2OWQzYjE0N2VhMGQzZTY1YiIsInVzZXJfaWQiOjF9.QcjZF7akrOYTM0reSBYpzf9jvbdcv60K7-3N0qcBWqs"
}
```

## Reminder!

You'll need the `Authorization` header with `Bearer <access_token>` to request the following endpoints.

## Regular user endpoints

Endpoints any user can call. 

### GET /products/
Requests the list of products created by the current user (or every product if the user is a superuser).

To optimize the requests, only the `id` and `url` fields are provided. To get more details about the entry, request the provided url.

Request
```http
GET http://localhost:8000/api/v1/products/
```

Response
```js
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "url": "http://localhost:8000/api/v1/products/1/"
        }
    ]
}
```

### POST /products/
Allows the user to create a new product.

Request
```http
POST http://localhost:8000/api/v1/products/
```

```js
{
    "title": "Example Product 2",
    "notification_email": "newexample@example.com"
}
```

Response
```js
{
    "id": 2,
    "title": "Example Product 2",
    "notification_email": "newexample@example.com",
    "activation_issued": false,
    "activation_approved": null
}
```

### GET /products/\<id\>/
Gets the data of a particular product if the user is the author or a superuser.

Request
```http
GET http://localhost:8000/api/v1/products/2/
```

Response
```js
{
    "id": 2,
    "title": "Example Product 2",
    "notification_email": "newexample@example.com",
    "activation_issued": false,
    "activation_approved": null
}
```

### PUT /products/\<id\>/
Updates the data of a particular product if the user is the author or a superuser.

Request
```http
PUT http://localhost:8000/api/v1/products/2/
```

```js
{
    "id": 2,
    "title": "New title",
    "notification_email": "newexample@example.com",
    "activation_issued": false,
    "activation_approved": null
}
```

Response
```js
{
    "id": 2,
    "title": "New title",
    "notification_email": "newexample@example.com",
    "activation_issued": false,
    "activation_approved": null
}
```

### DELETE /products/\<id\>/
Deletes the data of a particular product if the user is the author or a superuser.

Request
```http
DELETE http://localhost:8000/api/v1/products/2/
```

Response
```http
HTTP 204 No Content
```

### POST /products/\<id\>/activate/
Issues a product activation request to be reviewed by a superuser.

Request
```http
POST http://localhost:8000/api/v1/products/3/activate/
```

Response
```js
{
    "id": 3,
    "title": "A new product approaches",
    "notification_email": "hello@example.com",
    "activation_issued": true, // switched to true
    "activation_approved": null
}
```

### POST /products/\<id\>/cancel/
Cancels the product activation and removes it from the pending approvals.

To optimize the requests, only the `id` and `url` fields are provided. To get more details about the entry, request the provided url.

Request
```http
POST http://localhost:8000/api/v1/products/3/cancel/
```

Response
```js
{
    "id": 3,
    "url": "http://localhost:8000/api/v1/products/3/"
}
```

### GET /products/pending/
Shows all the pending products to be approved created by the user or every pending product if a superuser.

A product is considered pending if `activation_issued` is `true` and a superuser hasn't approved or rejected yet (`activation_approved` equal to `null`).

Request
```http
GET http://localhost:8000/api/v1/products/pending/
```

Response
```js
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "title": "A new product approaches",
            "notification_email": "hello@example.com",
            "activation_issued": true, // Issued
            "activation_approved": null // But not yet approved or rejected
        }
    ]
}
```

## Superuser endpoints

Endpoints only a superuser can call.

### POST /products/\<id\>/approve/
Approves the user's request. A product can only be accepted or rejected once.

Request
```http
POST http://localhost:8000/api/v1/products/3/approve/
```

Response
```js
{
    "id": 3,
    "title": "A new product approaches",
    "notification_email": "hello@example.com",
    "activation_issued": true,
    "activation_approved": true // now true
}
```

### POST /products/\<id\>/reject/
Rejects the user's request. A product can only be accepted or rejected once.

Request
```http
POST http://localhost:8000/api/v1/products/3/reject/
```

Response
```js
{
    "id": 3,
    "title": "A new product approaches",
    "notification_email": "hello@example.com",
    "activation_issued": true,
    "activation_approved": false // now false
}
```