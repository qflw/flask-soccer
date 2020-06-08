import unittest

from soccer import create_app, db
from soccer.model import User, Role
from flask import url_for, g


class RegisterTestCase(unittest.TestCase):
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

    def test_register_user_email_missing(self):
        ''' test invalid register email missing '''
        Role.insert_roles()
        User.insert_users()
        response = self.client.get(url_for('main.register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url_for('main.register'),
                                    data={"username": "invalid",
                                          "password": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"E-Mail is required.", response.data)
        self.client.get("/")
        self.assertIsNone(g.user)

    def test_register_user_username_missing(self):
        ''' test invalid register username missing '''
        Role.insert_roles()
        User.insert_users()
        response = self.client.get(url_for('main.register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url_for('main.register'),
                                    data={"email": "invalid",
                                          "password": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username is required.", response.data)
        self.client.get("/")
        self.assertIsNone(g.user)

    def test_register_user_password_missing(self):
        ''' test invalid register password missing '''
        Role.insert_roles()
        User.insert_users()
        response = self.client.get(url_for('main.register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url_for('main.register'),
                                    data={"email": "invalid",
                                          "username": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password is required.", response.data)
        self.client.get("/")
        self.assertIsNone(g.user)

    def test_register_user_already_existing(self):
        ''' test invalid register already exiting '''
        Role.insert_roles()
        User.insert_users()
        response = self.client.get(url_for('main.register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url_for('main.register'),
                                    data={"password": "password",
                                          "email": "invalid",
                                          "username": "user1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User user1 is already registered.", response.data)
        self.client.get("/")
        self.assertIsNone(g.user)
