from app import schemas
from app.config import settings
import pytest
from jose import jwt



def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login(test_user, client):
    res = client.post(
        '/login', data={
            'username': test_user['email'],
            "password": test_user['password']
        }
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload.get('user_id') == test_user['id']
    assert login_res.token_type == 'bearer'

    assert res.status_code

@pytest.mark.parametrize('email, password, status_code', [
    ("testcreateuser@gmail.com", "wrongpassword", 401),
    ("wrongemail@gmail.com", "password123", 401),
    ("wrongemail@gmail.com", "wrongpassword", 401)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        '/login', data={
            'username': email,
            'password': password
        }
    )
    assert res.status_code == status_code
