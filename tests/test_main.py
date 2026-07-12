"""單元測試 —— 用 FastAPI 的 TestClient，不用真的開 server。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_root_has_version():
    r = client.get("/")
    assert r.status_code == 200
    assert "version" in r.json()


def test_login_empty_email():
    # 對應 PR：空白 email 應回 400 + 錯誤訊息，而不是 500
    r = client.post("/login", json={"email": "", "password": "x"})
    assert r.status_code == 400
    assert r.json() == {"error": "email is required"}


def test_login_ok():
    r = client.post("/login", json={"email": "a@b.com", "password": "x"})
    assert r.status_code == 200
    assert "welcome" in r.json()["message"]
