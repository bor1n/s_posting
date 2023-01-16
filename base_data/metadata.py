from fastapi.testclient import TestClient

from db.base import database
from main import app
from models.user import UserIn

import json

@app.on_event("startup")
async def startup():
    await database.connect()



with TestClient(app) as client:
    # CREATE BASE USERS
    # =======================
    response = client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=UserIn(name='John', email='Jo1hn@sas.re', password='Johnpassword123', password2='Johnpassword123').dict(),
            )
    user_john = json.loads(response.text)
    print(response.request, response.text)
    client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=UserIn(name='David', email='David@sas.re', password='Davidpassword123', password2='Davidpassword123').dict(),
            )
    user_david = json.loads(response.text)
    print(response.request, response.text)
    client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=UserIn(name='Mark', email='Mark@sas.re', password='Markpassword123', password2='Markpassword123').dict(),
            )
    user_mark = json.loads(response.text)
    print(response.request, response.text)
    client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=UserIn(name='Orion', email='Orion@sas.re', password='Orionpassword123', password2='Orionpassword123').dict(),
            )
    user_orion = json.loads(response.text)
    client.post(
                "/users/",
                headers={'accept': 'application/json'},
                json=UserIn(name='Max', email='max@sas.re', password='Maxpassword123', password2='Maxpassword123').dict(),
            )
    user_max = json.loads(response.text)
    print(response.request, response.text)
    # =======================


