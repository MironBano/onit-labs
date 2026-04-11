FROM python:3.12-bookworm AS builder
WORKDIR /app
COPY pyproject.toml ./
COPY app ./app
RUN pip install --prefix=/install --no-cache-dir .

FROM python:3.12-slim-bookworm
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /install /usr/local
COPY app ./app
COPY pyproject.toml ./
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
