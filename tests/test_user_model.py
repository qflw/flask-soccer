import unittest

from soccer import create_app, db
from soccer.model import User, Role, Permission


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        Role.insert_roles()
        user1 = User(username="hans", password="123", email="123@123.com")
        self.assertEqual(user1.role.permissions, Permission.TIPPER)
        db.session.add(user1)

        user2 = User(username="hans1", password="123", email="1234@123.com")
        self.assertEqual(user2.role.permissions, Permission.TIPPER)
        db.session.add(user2)
        db.session.commit()

        users = User.query.all()
        self.assertEqual(len(users), 2)

        '''
        token = u1.generate_password_reset_token()
        self.assertFalse(u2.reset_password(token, 'notnotpassword'))
        self.assertTrue(u2.verify_password('notpassword'))
        '''
