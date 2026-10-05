import importlib
import json
from unittest import mock
from unittest.mock import patch, Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from .app.core.config import DATABASE_PASSWORD, DATABASE_USERNAME, DATABASE_HOST
from .app.core.database import engine, get_db
from .app.models.models import CachedData
from .app.utils import data_transformer
from .main import app

client = TestClient(app)

engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/test_db"
)


def override_get_db():
    try:
        db = Session(engine)
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def test_db():
    CachedData.metadata.create_all(bind=engine)
    yield
    CachedData.metadata.drop_all(bind=engine)

data_transformer = importlib.import_module('.app.utils.data_transformer', package="fastapi_test")


@patch.object(data_transformer, 'transformer_function')
def test_add_new_data(tf_mock, test_db):
    tf_mock.return_value = (
        [
            "first string", "second string", "third string", "other string", "another string", "last string"
        ],
        True
    )
    response = client.post(
        "/api/transform_list/",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "list_1": ["first string", "second string", "third string"],
                "list_2": ["other string", "another string", "last string"]
            }
        )
    )
    assert response.status_code == 200
    assert response.json() == 1