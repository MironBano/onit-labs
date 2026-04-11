"""Интеграционный функциональный тест CRUD через HTTP и реальную PostgreSQL."""

import uuid

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app

    with TestClient(app) as c:
        yield c


def test_health_ok(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_create_note_and_see_in_list(client: TestClient):
    title = f"CI-{uuid.uuid4().hex[:8]}"
    body = "текст из pytest"
    r = client.post("/notes/new", data={"title": title, "body": body}, follow_redirects=False)
    assert r.status_code == 303
    assert r.headers.get("location") == "/"

    r = client.get("/")
    assert r.status_code == 200
    html = r.text
    assert title in html
    assert body in html
