import datetime
import pytest

from fastapi.testclient import TestClient

from core.security import create_access_token
from main import app
from db.base import database
from models.token import Token


@app.on_event("startup")
async def startup():
    await database.connect()


def get_token(email):
    token = Token(
        access_token=create_access_token({"sub": email}),
        token_type="Bearer"
    )
    return f"{token.token_type} {token.access_token}"


class TestUsers:
    test_user = {
        "name": "string",
        "email": "test@example.com",
        "password": "stringst",
        "password2": "stringst"
    }

    def test_create_user(self):
        with TestClient(app) as client:
            response = client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=self.test_user,
            )
            assert response.status_code == 200
            created_user_data = response.json()
            pytest.shared = created_user_data
            assert created_user_data['name'] == self.test_user['name']
            assert created_user_data['email'] == self.test_user['email']
            assert isinstance(created_user_data['id'], int)
            assert created_user_data['created_at'] == created_user_data['updated_at']
            assert datetime.datetime.strptime(created_user_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            assert datetime.datetime.strptime(created_user_data['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

    def test_create_duplicate_user(self):
        with TestClient(app) as client:
            response = client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=self.test_user,
            )
            assert response.status_code == 409
            assert response.json() == {
                'detail': 'Account already registered with this email address'
            }

    def test_get_list(self):
        with TestClient(app) as client:
            response = client.get(
                "/users/",
                headers={'accept': 'application/json'},
            )
            assert response.status_code == 200
            created_user_data = pytest.shared
            assert response.json() == [created_user_data]

    @pytest.mark.parametrize('parameter', ['limit', 'offset'])
    def test_get_list_negative_values(self, parameter):
        with TestClient(app) as client:
            response = client.get(
                f"/users/?{parameter}=-1",
                headers={'accept': 'application/json'},
            )
            assert response.status_code == 422
            assert response.json() == {
                  "detail": [
                    {
                      "loc": [
                        "query",
                        parameter
                      ],
                      "msg": "ensure this value is greater than or equal to 0",
                      "type": "value_error.number.not_ge",
                      "ctx": {
                        "limit_value": 0
                      }
                    }
                  ]
                }

    def test_update_user(self):
        with TestClient(app) as client:
            _data = self.test_user.copy()
            _data.update({'name': 'John'})

            response = client.patch(
                "/users/",
                headers={
                    'accept': 'application/json',
                    'Authorization': get_token(self.test_user["email"]),
                    'Content-Type': 'application/json',
                },
                json=_data
            )
            assert response.status_code == 200
            updated_user_data = response.json()
            pytest.shared = updated_user_data
            assert updated_user_data['name'] == _data['name']
            assert updated_user_data['email'] == _data['email']
            assert isinstance(updated_user_data['id'], int)
            assert updated_user_data['created_at'] != updated_user_data['updated_at']
            assert datetime.datetime.strptime(updated_user_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            assert datetime.datetime.strptime(updated_user_data['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

    def test_update_user_not_auth(self):
        with TestClient(app) as client:
            _data = self.test_user.copy()
            _data.update({'name': 'John'})

            response = client.patch(
                "/users/",
                headers={'accept': 'application/json'},
                json=_data,
            )
            assert response.status_code == 403
            assert response.json() == {
                "detail": "Not authenticated"
            }
