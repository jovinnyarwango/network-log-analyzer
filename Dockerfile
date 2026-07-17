# Minimal Python base image (~50MB vs ~1GB for full python)
FROM python:3.12-slim

# All work happens in /app inside the container
WORKDIR /app

# Copy only the script — data comes in at runtime, never baked into the image
COPY log_analyzer.py .

# The container IS this command; docker run arguments get appended to it
ENTRYPOINT ["python", "log_analyzer.py"]
