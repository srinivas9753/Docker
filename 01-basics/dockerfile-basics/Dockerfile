# Base image
FROM python:3.12-slim

# Build-time variable (can be changed with --build-arg)
ARG APP_VERSION=1.0

# Run-time environment variable
ENV APP_NAME="Srinivas"

# Working directory inside the container
WORKDIR /app

# Copy the script into the image
COPY app.py .

# Run a command at build time (creates a layer)
RUN echo "Building version ${APP_VERSION}"

# Default command when the container starts
CMD ["python", "app.py"]