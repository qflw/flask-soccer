import unittest

from soccer import create_app, db


class CommandTestCase(unittest.TestCase):
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

    def test_command_invalid(self):
        response = self.client.get('/action/invalid')
        self.assertEqual(response.status_code, 404)

    def test_command_update(self):
        response = self.client.get('/action/update', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AUTH_TOKEN not set", response.data)
