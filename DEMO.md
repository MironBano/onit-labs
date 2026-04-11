# Демонстрация лабораторных ОНИТ (ЛР1–4)

## Подготовка (один раз)

1. Установите [Docker Desktop](https://www.docker.com/products/docker-desktop/) и включите **WSL2**, если требуется.
2. В корне репозитория: скопируйте `cp .env.example .env` (Windows: `Copy-Item .env.example .env`).

## ЛР1–2: приложение с ORM и Docker

1. Запуск стека:

   ```bash
   docker compose up --build
   ```

2. Откройте в браузере: `http://127.0.0.1:8000/` — список заметок, создание, редактирование, удаление (CRUD).
3. Проверка готовности контейнеров:

   ```bash
   docker compose ps
   ```

   У сервисов `db` и `app` в колонке состояния должны быть **healthy**.

4. Быстрый smoke (после остановки compose при необходимости снова `up`):

   - Linux/macOS: `bash scripts/smoke_compose.sh`
   - Windows PowerShell: `.\scripts\smoke_compose.ps1`

## ЛР3: CI/CD на GitHub

1. Создайте репозиторий на GitHub и выполните `git push` в ветку `main` или `master`.
2. Откройте вкладку **Actions** — workflow **CI/CD** должен завершиться зелёным.
3. (Опционально) В **Settings → Secrets and variables → Actions** добавьте secrets/variables по списку в [docs/SECRETS.md](docs/SECRETS.md).
4. После push: **Packages** (GHCR) — опубликованный образ приложения.

## ЛР4: Nginx и round-robin

1. В отдельном терминале:

   ```bash
   cd lr4
   docker compose up --build
   ```

2. Откройте в браузере несколько раз подряд: `http://127.0.0.1:8080/` — при отключённом кэше или «жёстком» обновлении может меняться заголовок **Нода 1 / 2 / 3**.

3. Наглядная проверка round-robin (новое TCP-соединение на каждый запрос):

   **PowerShell:**

   ```powershell
   1..12 | ForEach-Object {
     (Invoke-WebRequest -Uri "http://127.0.0.1:8080/" -UseBasicParsing).Content -match "Нода (\d)" | Out-Null
     $Matches[1]
   }
   ```

   **bash:**

   ```bash
   for i in $(seq 1 12); do
     curl -s http://127.0.0.1:8080/ | grep -oP 'Нода \K[0-9]+'
   done
   ```

   Ожидается чередование **1, 2, 3, 1, 2, 3, …** (при отсутствии ошибок маршрутизации).

4. Остановка:

   ```bash
   docker compose down
   ```

## Локальные тесты pytest (без GitHub)

1. Поднимите только БД и приложение или только БД:

   ```bash
   docker compose up -d db
   ```

2. Убедитесь, что порт **5433** проброшен (см. `docker-compose.yml`) и совпадает с `DATABASE_URL` в окружении.

3. Установите зависимости и запустите тесты:

   ```bash
   pip install -e ".[dev]"
   set DATABASE_URL=postgresql://onit:onit_local_password@127.0.0.1:5433/onitdb
   python -m pytest -v
   ```

   (В PowerShell: `$env:DATABASE_URL="..."` перед `pytest`.)
