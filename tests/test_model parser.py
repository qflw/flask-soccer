import unittest

from soccer import create_app, db
from soccer.model import parse_json, Match, Team, Event, Group


class ParserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_parser_em(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(parse_json, ['soccer/assets/2018_matches.json'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'parsing done\n')
        matches = Match.query.all()
        self.assertEqual(len(matches), 36)
        teams = Team.query.all()
        self.assertEqual(len(teams), 24)
        events = Event.query.all()
        self.assertEqual(len(events), 1)
        groups = Group.query.all()
        self.assertEqual(len(groups), 6)

    def test_parser_bl(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(parse_json, ['soccer/assets/2002_matches.json'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'parsing done\n')
