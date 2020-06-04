import unittest

from soccer import create_app, db
from soccer.model import User, Role
from flask import url_for, g


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_user(self):
        ''' test invalid login '''
        Role.insert_roles()
        User.insert_users()
        response = self.client.get(url_for('main.login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/login", data={"username": "username",
                                                    "password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username/password", response.data)
        self.client.get("/")
        self.assertIsNone(g.user)

    def test_login_user_valid(self):
        ''' test valid login '''
        Role.insert_roles()
        User.insert_users()
        response = self.client.get(url_for('main.login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/login", data={"username": "user1",
                                                    "password": "pass"},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(g.user)
