# ОНИТ — лабораторные 1–4

Веб-приложение **«Заметки»**: CRUD через **SQLAlchemy ORM**, PostgreSQL, минимальный HTML-интерфейс (**FastAPI** + **Jinja2**). Docker Compose (ЛР2), GitHub Actions + GHCR (ЛР3), отдельный стек **lr4** с **Nginx** и round-robin.

Текст задания: [Labs_task.txt](Labs_task.txt).

**Теория и объяснения «с нуля»** (в т.ч. если вы с Android и не знакомы с Docker): [docs/TEORIYA_ONIT.md](docs/TEORIYA_ONIT.md).

## Требования

- Python **3.11+** (локально — для pytest).
- **Docker** и **Docker Compose** v2.

## Быстрый старт (ЛР1–2)

```bash
cp .env.example .env
docker compose up --build
```

Откройте **http://127.0.0.1:8000/** .

- API проверки готовности: `GET /health`
- БД доступна с хоста на порту **5433** (для локальных тестов).

Остановка: `docker compose down`.

Если в браузере **ERR_CONNECTION_REFUSED** на порту 8000: выполните `docker compose ps` — контейнер `app` должен быть **Up (healthy)**. Если вы перед этим задавали `$env:DATABASE_URL` для pytest, откройте **новое** окно терминала или сбросьте переменную (`Remove-Item Env:DATABASE_URL`), затем снова `docker compose up -d`.

## Тесты

```bash
pip install -e ".[dev]"
```

Поднимите БД (`docker compose up -d db`), затем с тем же паролем, что в `.env`:

```bash
export DATABASE_URL=postgresql://onit:onit_local_password@127.0.0.1:5433/onitdb
python -m pytest -v
```

## ЛР4 (Nginx)

```bash
cd lr4
docker compose up --build
```

Балансировщик: **http://127.0.0.1:8080/** — см. [DEMO.md](DEMO.md).

## CI/CD и секреты

- Workflow: [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)
- Секреты/variables: [docs/SECRETS.md](docs/SECRETS.md)
- Сценарий защиты: [DEMO.md](DEMO.md)

## GitHub

```bash
git init
git add .
git commit -m "ОНИТ: ЛР1–4"
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

После первого push проверьте **Actions** и при необходимости настройте **Packages** (права `packages: write` у `GITHUB_TOKEN` для GITHUB_TOKEN уже заданы в workflow).

## Структура

| Путь | Описание |
|------|----------|
| `app/` | Приложение ЛР1–2 |
| `templates/` | Шаблоны Jinja2 |
| `tests/` | Pytest + интеграция с PostgreSQL |
| `lr4/` | ЛР4: три ноды + Nginx |
| `scripts/` | Smoke-проверка compose |
