#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  echo "Создайте .env из .env.example: cp .env.example .env"
  exit 1
fi

docker compose up -d --build
echo "Ожидание health приложения..."
for i in $(seq 1 40); do
  if curl -fsS "http://127.0.0.1:8000/health" >/dev/null 2>&1; then
    echo "OK /health"
    break
  fi
  sleep 1
  if [[ "$i" == "40" ]]; then
    echo "Таймаут health"
    docker compose ps
    docker compose logs --tail=80 app
    exit 1
  fi
done

curl -fsS -o /dev/null -X POST "http://127.0.0.1:8000/notes/new" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "title=smoke&body=from-script"
curl -fsS "http://127.0.0.1:8000/" | grep -q smoke
echo "Smoke: CRUD create + список OK"
