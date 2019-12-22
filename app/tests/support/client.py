from ... import app, db
from ...models import User

"""
Bootstrap application for testing - use this when creating a client fixture
return test client
"""


def get_test_client():

    # Drop all tables and recreate schema
    db.drop_all()
    db.create_all()

    # Populate with fixtures
    user = User()
    user.email = "testy@testy.com"
    user.name_first = "Testy"
    user.name_last = "McTesterson"
    user.zip = "97111"
    db.session.add(user)
    db.session.commit()

    return app.test_client()
