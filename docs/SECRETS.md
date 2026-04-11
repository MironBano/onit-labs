# Секреты и переменные GitHub (ЛР3)

Имена ниже **совпадают** с переменными локального `.env` из ЛР2, чтобы выполнить требование вынести учётные данные в GitHub.

## Repository secrets (Settings → Secrets and variables → Actions)

| Имя secret | Назначение |
|------------|------------|
| `POSTGRES_USER` | Пользователь БД (необязательно: если не задан, в CI используется `test_user`) |
| `POSTGRES_PASSWORD` | Пароль БД (необязательно: если не задан, в CI используется `test_password`) |

## Repository variables (та же страница, вкладка Variables)

| Имя variable | Назначение |
|--------------|------------|
| `POSTGRES_DB` | Имя базы (необязательно: если не задано, в CI используется `test_db`) |

## Как это связано с workflow

В [.github/workflows/ci-cd.yml](../.github/workflows/ci-cd.yml) job **test** подставляет значения в `DATABASE_URL` через выражения `secrets.*` и `vars.*` с **запасными значениями по умолчанию**, как в методичке для PR.

Сервис PostgreSQL внутри GitHub Actions по умолчанию создаётся с учётными данными `test_user` / `test_password` / `test_db`. Если вы задаёте свои secrets/vars, **убедитесь**, что они совпадают с теми же учётными данными, которые ожидает сервис `postgres` в workflow (при необходимости отредактируйте блок `services.postgres.env` в YAML под ваши значения).

## Публикация образа (CD)

Job **build** входит в GitHub Container Registry с **`GITHUB_TOKEN`** (отдельный PAT не нужен). После успешного push откройте **Packages** в репозитории.
