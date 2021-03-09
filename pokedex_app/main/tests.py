from unittest import TestCase
from pokedex_app import app, db, bcrypt
from pokedex_app.models import User

# How to run auth tests:
# python -m unittest pokedex_app.auth.tests

# How to run all tests:
# python -m unittest discover
# OR just:
# python -m unittest
# The two are equivalent:
# https://docs.python.org/3/library/unittest.html#test-discovery

#################################################
# Setup
#################################################

def add_user(user):
    password_hash = bcrypt.generate_password_hash(user['password']).decode('utf-8')
    user = User(username=user['username'], password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup).""" 

    # Use self.test_account OR self.__class__.test_account
    # to make it explicit that this is a class variable.
    test_account = {
        'username': 'username',
        'password': 'password'
    }

    def setUp(self):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage(self):
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You are browsing anonymously", response_text)
