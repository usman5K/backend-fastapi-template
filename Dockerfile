# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the entire application code including scripts
COPY . .

# Ensure the script has execute permissions
RUN chmod +x ./scripts/start-backend.sh

# Expose the port your application runs on
EXPOSE 8000

# Set the entry point to the start script
ENTRYPOINT ["./scripts/start-backend.sh"]
