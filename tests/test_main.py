from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 201  # Deliberate failure for Lab 4 Task C
    assert "message" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_missing_item():
    assert client.get("/items/999").status_code == 404
