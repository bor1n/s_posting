from db import metadata, engine
from fastapi.testclient import TestClient

from db.base import database
from main import app



def pytest_sessionfinish(session, exitstatus):
    metadata.drop_all(bind=engine)
    """ whole test run finishes. """