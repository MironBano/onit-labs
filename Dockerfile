# --- Сборка зависимостей ---
FROM python:3.12-bookworm AS builder
WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY pyproject.toml ./
COPY app ./app
RUN pip install --prefix=/install --no-cache-dir .

# --- Финальный образ ---
FROM python:3.12-slim-bookworm
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local
COPY app ./app
COPY templates ./templates
COPY pyproject.toml ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
