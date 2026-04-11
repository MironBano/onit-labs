import os

# Должно выполниться до импорта приложения (при коллекции тестов).
# Локально: поднимите `docker compose up -d` и используйте те же креды, что в `.env.example` (порт БД 5433).
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://onit:onit_local_password@127.0.0.1:5433/onitdb",
)
