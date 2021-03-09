from unittest import TestCase
from pokedex_app import app, db

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

# N/A

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup).""" 

    # Use self.test_account OR self.__class__.test_account
    # to make it explicit that this is a class variable.
    test_region = {
        'name': 'Hoenn',
        'photo_url': 'https://cdn.bulbagarden.net/upload/8/85/Hoenn_ORAS.png',
        'description': 'I love pokemon Emerald :)'
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

    def test_new_region(self):
        response = self.app.get('/new_region')
        response_text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Region Name", response_text)

        response = self.app.post('/new_region', data=self.test_region)
        response_text = response.get_data(as_text=True, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_region['name'], response.location)

        response = self.app.get(f'/region/{self.test_region["name"]}')
        response_text = response.get_data(as_text=True)
        self.assertIn(self.test_region['name'], response_text)
        self.assertEqual(response.status_code, 200)
