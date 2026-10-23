# tests/test_health.py — the real tests the Lab 4 pipeline runs on every pull request.
#
# Lab 4, Task D: make ONE of these fail on purpose (e.g. change 200 to 201),
# push it on a branch, and show the red check blocking the merge.
from fastapi.testclient import TestClient

from app.main import APP_VERSION, app

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_home_reports_version():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["app"] == "notes"
    assert body["version"] == APP_VERSION
