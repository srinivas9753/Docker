# Hello World (Docker)

Simple Python app that prints a message, packaged in Docker.

## Build
```bash
docker build -t hello-world-py:1.0 .
```

## Run
```bash
docker run --rm hello-world-py:1.0
```

## Expected output
```
Hello, Docker World!
```