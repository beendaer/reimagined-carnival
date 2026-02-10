FROM python:3.12-slim
WORKDIR /app
RUN addgroup --gid 1001 app && adduser --uid 1001 --gid 1001 --shell /bin/sh --disabled-password app
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s CMD wget -q --spider http://localhost:8000/health || exit 1
ENV UVICORN_APP=src.api:app
CMD ["sh", "-c", "uvicorn ${UVICORN_APP} --host 0.0.0.0 --port 8000"]
FROM python:3.12-alpine
WORKDIR /app
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
RUN apk add --no-cache wget
COPY . .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s CMD wget -q --spider http://localhost:3000/health || exit 1
CMD ["python", "app.py"]
