from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask.cli import with_appcontext
from . import db
import click
import json
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from soccer.calculator import calc_points


class Permission:
    TIPPER = 0x01
    ADMINISTER = 0xff


class Role(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = Permission.TIPPER

    @staticmethod
    def insert_roles():
        db.session.add(Role(name='tipper'))
        db.session.add(Role(name='admin', permissions=Permission.ADMINISTER))
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = Column(String(120), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(name='tipper').first()

    @staticmethod
    def insert_users():
        db.session.add(User(username='user1', email="1@1.de", password='pass'))
        db.session.add(User(username='user2', email="2@1.de", password='pass'))
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_points(self):
        points = 0
        for bet in self.bets:
            points += calc_points(bet)
        return points

    def get_points_for_match(self, match):
        points = 0
        for bet in self.bets:
            if bet.match == match:
                points += calc_points(bet)
        return points

    def has_write_permission(self):
        """ TODO check permissions more precisly """
        return self.role.permissions == Permission.ADMINISTER

    def __repr__(self):
        return '<User %r>' % self.username


class Team(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    short_name = Column(String(3), unique=True, nullable=False)

    def __repr__(self):
        return '<Team %r %r>' % (self.name, self.short_name)


class Bet(db.Model):
    id = Column(Integer, primary_key=True)
    bet = Column(String(50), unique=False, nullable=True)
    match_id = Column(Integer, ForeignKey('match.id'), nullable=False)
    match = db.relationship('Match', backref=db.backref('bets', lazy=True))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bets', lazy=True))

    def __repr__(self):
        return '<Bet %r %r %r>' % (self.user, self.match, self.bet)


class Match(db.Model):
    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    home = db.relationship('Team',  foreign_keys='Match.home_id')
    away_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    away = db.relationship('Team', foreign_keys='Match.away_id')
    result = Column(String(50), unique=False, nullable=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=True)
    group = db.relationship('Group', backref=db.backref('matches', lazy=True))
    datetime = Column(DateTime, unique=False, nullable=True)

    def __repr__(self):
        return '<Match %r %r %r>' % (self.home, self.away, self.datetime)

    def get_bet_for_user(self, user):
        return Bet.query.filter_by(match_id=self.id, user_id=user.id).first()


class Group(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False, nullable=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('groups', lazy=True))

    def __repr__(self):
        return '<Group %r>' % (self.name)


class Event(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False, nullable=True)

    def __repr__(self):
        return '<Event %r>' % (self.name)


def init_db():
    db.drop_all()
    db.create_all()
    admin = Role(name="Admin", permissions=Permission.ADMINISTER)
    db.session.add(admin)
    tipper = Role(name="Tipper", permissions=Permission.TIPPER)
    db.session.add(tipper)

    # adding some users
    admin_user = User(username="admin", password="password",
                      email="email1@domain.com", role=admin)
    db.session.add(admin_user)
    db.session.add(User(username="dummy1", password="password",
                        email="email2@domain.com", role=tipper))
    db.session.add(User(username="dummy2", password="password",
                        email="email3@domain.com", role=tipper))

    em = Event(name="EM")
    groupA = Group(name="A", event=em)
    db.session.add(groupA)

    # adding some teams
    '''
    germany = Team(name="Germany", short_name="GER")
    france = Team(name="France", short_name="FRA")
    db.session.add(germany)
    db.session.add(france)

    england = Team(name="England", short_name="ENG")
    sweden = Team(name="Sweden", short_name="SWE")

    db.session.add(england)
    db.session.add(sweden)
    db.session.add(Team(name="Italy", short_name="ITA"))

    match_ger_fra = Match(home=germany, away=france, group=groupA,
                          datetime=datetime(2006, 11, 21, 16, 30))
    db.session.add(match_ger_fra)
    db.session.add(Match(home=england, away=sweden, group=groupA,
                         datetime=datetime(2006, 11, 22, 16, 30)))

    bet1 = Bet(bet="1:2", user=admin_user, match=match_ger_fra)
    db.session.add(bet1)
    '''
    db.session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('parse-json')
@click.argument("input_file", type=click.Path())
@with_appcontext
def parse_json(input_file):
    """parse"""
    input = open(input_file)
    data = json.load(input)
    matches = data["matches"]
    for match in matches:
        home = match["homeTeam"]
        away = match["awayTeam"]
        if not Team.query.filter_by(id=home["id"]).first():
            name = home["name"]
            t1 = Team(id=home["id"], name=name, short_name=name[:3])
            db.session.add(t1)

        if not Team.query.filter_by(id=away["id"]).first():
            name = away["name"]
            t1 = Team(id=away["id"], name=name, short_name=name[:3])
            db.session.add(t1)

        m = Match.query.filter_by(id=match["id"]).first()
        if m:
            m.group_id = 1
        else:
            date = datetime.strptime(match["utcDate"], '%Y-%m-%dT%H:%M:%SZ')
            m1 = Match(id=match["id"], home_id=home["id"],
                       away_id=away["id"], datetime=date, group_id=1)
            db.session.add(m1)

    db.session.commit()
    click.echo('parsing done')


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(parse_json)
    # register function global for jinja
    app.jinja_env.globals.update(getBet=getBet)


def getBet(match, user):
    return Bet.query.filter_by(match_id=match.id, user_id=user.id).first()
