import pytest

from src import app, models

from .utils import ApiClient
from uuid import uuid4


@pytest.fixture(autouse=True)
def autouse_fixtures():
    models.db.drop_all()
    models.db.create_all()

    yield

    models.db.session.close()


# TODO: Do we want this?
# @pytest.fixture(autouse=True)
# def request_context(app):
#     with app.test_request_context():
#         yield


@pytest.fixture
def client():
    app.app.test_client_class = ApiClient
    with app.app.test_client() as client:
        user_id = uuid4()
        user = models.User(id=user_id, name="Test user", email="test@example.com")
        models.db.session.add(user)
        models.db.session.commit()
    
        client.set_authenticated_user_id(user_id)
        yield client


@pytest.fixture
def unauthenticated_client():
    app.app.test_client_class = ApiClient
    with app.app.test_client() as client:
        yield client