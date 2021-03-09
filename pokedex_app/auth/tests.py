from unittest import TestCase
from pokedex_app import app, db, bcrypt
from pokedex_app.models import User

# How to run auth tests:
# python -m unittest pokedex_app.auth.tests

# How to run all tests:
# python -m unittest discover

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

    test_account_invalid_password = {
        'username': 'username',
        'password': 'nope'
    }

    def setUp(self):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup_valid(self):
        post_data = self.test_account

        response = self.app.post('/signup', data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

        added_user = User.query.filter_by(username='username').first()
        self.assertIsNotNone(added_user)
        self.assertEqual(added_user.username, 'username')
        self.assertTrue(bcrypt.check_password_hash(added_user.password, 'password'))

    def test_signup_existing_user(self):
        add_user(self.test_account)
        post_data = self.test_account

        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("That username is taken. Please try another one.", response_text)

    def test_login_valid(self):
        add_user(self.test_account)
        post_data = self.test_account

        response = self.app.post('/login', data=post_data, follow_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("You are logged in", response_text)

    def test_login_invalid_username(self):
        post_data = self.test_account

        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("That username is not signed up.", response_text)

    def test_login_invalid_password(self):
        add_user(self.test_account)
        post_data = self.test_account_invalid_password

        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)

        self.assertIn("That password is incorrect.", response_text)

    def test_logout(self):
        add_user(self.test_account)
        post_data = self.test_account

        response = self.app.post('/login', data=post_data)
        self.assertEqual(response.status_code, 302)

        response = self.app.get('/logout', follow_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Log In', response_text)
        self.assertNotIn('Log Out', response_text)
