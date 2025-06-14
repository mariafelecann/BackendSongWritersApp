import pytest
from app import create_app
from database.database import Base, DatabaseSingleton
from flask import g

@pytest.fixture
def client():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    app.config['URI'] = "sqlite:///:memory:"

    db_singleton = DatabaseSingleton(app)
    engine = db_singleton.engine

    with app.test_client() as client:
        with app.app_context():
            Base.metadata.create_all(engine)

            yield client
            Base.metadata.drop_all(engine)
