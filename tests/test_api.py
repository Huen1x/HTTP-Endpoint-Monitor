import os
import sys

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "src"))
)
from fastapi.testclient import TestClient
from main import app
from models import Endpoint, SessionLocal, init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    db = SessionLocal()
    db.query(Endpoint).delete()
    db.commit()
    db.close()
    yield
    db = SessionLocal()
    db.query(Endpoint).delete()
    db.commit()
    db.close()


@pytest.fixture
def client():
    return TestClient(app)


def test_add_and_list_endpoint(client):
    url = "https://httpbin.org/status/200"
    response = client.post("/endpoints/", json={"url": url})
    assert response.status_code == 201
    body = response.json()
    assert body["url"] == url
    assert body["count"] == 0
    response_2 = client.get("/endpoints/?sort=asc")
    lst = response_2.json()
    assert isinstance(lst, list)
    assert len(lst) == 1
    assert lst[0]["url"] == url


def test_check_endpoint_success(client):
    response = client.post(
        "/endpoints/", json={"url": "https://httpbin.org/status/200"}
    )
    endpoint_id = response.json()["id"]
    response_2 = client.post(f"/endpoints/{endpoint_id}/check")
    assert response_2.status_code == 200
    assert response_2.json()["counted"] is True
    response_3 = client.get("/endpoints/?sort=asc")
    assert response_3.json()[0]["count"] == 1


def test_check_endpoint_failure(client):
    response = client.post(
        "/endpoints/", json={"url": "https://httpbin.org/status/500"}
    )
    eid = response.json()["id"]
    response_2 = client.post(f"/endpoints/{eid}/check")
    assert response_2.status_code == 200
    assert response_2.json()["counted"] is False
    response_3 = client.get("/endpoints/?sort=asc")
    assert response_3.json()[0]["count"] == 0


def test_delete_endpoint(client):
    response = client.post(
        "/endpoints/", json={"url": "https://httpbin.org/status/200"}
    )
    endpoint_id = response.json()["id"]
    response_2 = client.delete(f"/endpoints/{endpoint_id}")
    assert response_2.status_code == 204
    response_3 = client.get("/endpoints/")
    assert response_3.json() == []
