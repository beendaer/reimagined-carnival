# Production Dockerfile - Python 3.12-slim single-stage
# Per PROJECT_STATUS.md recommendation: single-stage, Python 3.12-slim, port 8000
FROM python:3.14-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY asgi.py .

# Environment configuration
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Start uvicorn server
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}"]

