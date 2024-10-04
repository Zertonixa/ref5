import pytest
from conftest import client
from httpx import AsyncClient

def test_post_breed():
    response = client.post("/breed", json={
    "description": "test",
    "origin": "test"
    })

    assert response.status_code == 200

def test_get_breed():
    response = client.get("/breed")
    assert response.status_code == 200

def test_post_kitten():
    response = client.post("/kitten", json={
    "name": "test_kitten",
    "breedID": 1,
    "age": 0,
    "color": "test_color",
    "description": "test_description"
    })
    assert response.status_code == 200

def test_get_kitten():
    response = client.get("/kitten")
    assert response.status_code == 200

def test_put_kitten():
    response = client.put("/kitten/1", json={
    "name": "test_kitten1",
    "breedID": 1,
    "age": 0,
    "color": "test_color",
    "description": "test_description"
    })
    assert response.status_code == 200


def test_delete_kitten():
    response = client.delete("/kitten/1")
    assert response.status_code == 200

def test_delete_breed():
    response = client.delete("/breed/1")
    assert response.status_code == 200

