"""Тесты API: создание, получение, удаление и ошибки валидации."""
import pytest
from fastapi.testclient import TestClient

import notes_api as api


@pytest.fixture
def client():
    # Каждый тест получает независимое хранилище.
    api.notes.clear()
    api.next_id = 1
    with TestClient(api.app) as test_client:
        yield test_client


def test_create_and_get_note(client):
    response = client.post("/notes", json={"text": "Купить хлеб"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "text": "Купить хлеб"}
    response = client.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "text": "Купить хлеб"}


def test_missing_note(client):
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Заметка не найдена"


def test_delete_note(client):
    client.post("/notes", json={"text": "Заметка"})
    response = client.delete("/notes/1")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/notes/1").status_code == 404
    assert client.delete("/notes/1").status_code == 404


def test_invalid_note(client):
    assert client.post("/notes", json={"text": ""}).status_code == 422
    assert client.post("/notes", json={}).status_code == 422
    assert client.post("/notes", json={"text": "x" * 201}).status_code == 422


def test_invalid_id(client):
    assert client.get("/notes/not-a-number").status_code == 422


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Создать" in response.text
    assert "Получить" in response.text
    assert "Удалить" in response.text
