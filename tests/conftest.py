"""Test setup: mock Gemini and use a throwaway SQLite file. Must run before the app is imported."""
import os
import tempfile

_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["FITBUDDY_MOCK_AI"] = "true"
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}"
os.environ.pop("GOOGLE_API_KEY", None)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as c:  # runs lifespan -> creates tables
        yield c


FORM = {
    "username": "Alex",
    "user_id": "alex_01",
    "age": "28",
    "weight": "72.5",
    "goal": "Muscle Gain",
    "intensity": "medium",
}
