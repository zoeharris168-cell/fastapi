

from app import schemas
from .database import client, session
def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello world!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "testcreateuser@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "testcreateuser@gmail.com"
    assert res.status_code == 201

def test_login(client):
    res = client.post(
        '/login', data={
            'username': 'testcreateuser@gmail.com',
            "password": "password123"
        }
    )
    assert res.status_code