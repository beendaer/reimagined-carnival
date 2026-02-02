FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY src/ src/
ENV PYTHONUNBUFFERED=1
EXPOSE $PORT
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "$PORT"]
