import unittest

from soccer import create_app, db
from soccer.model import Role, Permission


class RoleModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_default_permissions(self):
        tipper = Role(name="tipper")
        self.assertEqual(tipper.permissions, Permission.TIPPER)

    def test_full_permissions(self):
        tipper = Role(name="tipper", permissions=Permission.ADMINISTER)
        self.assertEqual(tipper.permissions, Permission.ADMINISTER)

    def test_add_to_db(self):
        admin = Role(name="admin", permissions=Permission.ADMINISTER)
        db.session.add(admin)
        db.session.commit()

        roles = Role.query.all()
        self.assertEqual(len(roles), 1)
