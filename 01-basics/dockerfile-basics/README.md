# Dockerfile Basics

Practice of the main Dockerfile instructions.

| Instruction | What it does | Example |
|---|---|---|
| FROM | Base image | `FROM python:3.12-slim` |
| WORKDIR | Sets working folder in the container | `WORKDIR /app` |
| COPY | Copies files from host into image | `COPY app.py .` |
| RUN | Runs a command at build time | `RUN echo "hi"` |
| ENV | Sets a run-time environment variable | `ENV APP_NAME="Srinivas"` |
| ARG | Sets a build-time variable | `ARG APP_VERSION=1.0` |
| CMD | Default command at container start | `CMD ["python", "app.py"]` |

## Build
```bash
docker build -t dockerfile-basics:1.0 .
```

## Run
```bash
docker run --rm dockerfile-basics:1.0
docker run --rm -e APP_NAME="DevOps" dockerfile-basics:1.0
```

## Key points
- ARG exists only while building; ENV is available when the container runs.
- Every instruction creates a layer.
- `.dockerignore` keeps unwanted files out of the build.