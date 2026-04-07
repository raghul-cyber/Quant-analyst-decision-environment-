FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

COPY . .

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:7860/health || exit 1

CMD ["uvicorn", "env:app", "--host", "0.0.0.0", "--port", "7860"]
