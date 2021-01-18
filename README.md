# Backend Assessment

Backend challenge for interview process of the Junior Backend Dev position at T10.

## Instructions

The instructions for the challenge can be found [here](Instructions.md).

## The solution

The solution leverages Python, Django and the Django Rest Framework to create an API that satisfies the provided use cases. PostgreSQL is the choice for the DMBS.

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

See the [full API Reference](api-reference.md) for a documentation of the endpoints.

## Running the tests

The project has a healthy amount of tests (mainly for the view logic). To run them, use the following command whilst the containers are running.

```bash
docker exec -it automatic_debit_api sh -c "python manage.py test"
```