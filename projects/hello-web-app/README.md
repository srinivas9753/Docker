# Django Hello App (Docker)

Simple Django web app with an HTML template page, running in a Docker container built from an Ubuntu base image.

## Build
```bash
docker build -t django-hello-app:1.0 .
```

## Run
```bash
docker run --rm -p 8000:8000 --name django-hello-app django-hello-app:1.0
```
Open http://localhost:8000

## Run from Docker Hub
```bash
docker run --rm -p 8000:8000 srini8899/django-hello-app:1.0
```

## What I learned
- Django project structure and templates
- Dockerfile for a Python web app
- `0.0.0.0:8000` and `-p 8000:8000` to reach the app from the browser