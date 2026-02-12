# Development/Infra Dockerfile - Python 3.12-slim
# Aligned with root Dockerfile for consistency
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -g 1001 app && useradd -u 1001 -g app -s /bin/sh -m app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Switch to non-root user
USER app

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

# Start uvicorn server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

