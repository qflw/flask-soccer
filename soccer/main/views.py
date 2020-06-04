from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    g,
    url_for,
    flash,
    abort,
    current_app
)
from soccer.model import Event, User, Role, Bet, Match
from soccer import db
import json
import os.path
import urllib
# from markupsafe import escape

main = Blueprint('main', __name__)


@main.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
    else:
        g.user = None


@main.before_app_request
def load_data_from_json():
    fname = current_app.config["JSON_DATA_FILENAME"]
    if os.path.isfile(fname):
        json_file = open(fname)
        if json_file:
            g.event_data = json.load(json_file)
        else:
            g.event_data = None


@main.route('/')
def event():
    '''
    if 'username' in session:
        return "Hello, World %s" % escape(session['username'])
    '''

    users = User.query.all()

    def sort_by_points(elem):
        return elem.get_points()

    users.sort(reverse=True, key=sort_by_points)

    display_user = None
    user_id = request.args.get('user_id')
    if user_id:
        display_user = User.query.filter_by(id=user_id).first()

    event = Event.query.filter_by(id=2018).first()
    if event:
        return render_template('event.html',
                               event=event,
                               display_user=display_user,
                               ranked_users=users)

    flash("No event was found")
    return render_template('event.html')


@main.route('/matches')
def matches():
    '''
    display matches loaded from the json file
    '''
    return render_template('matches.html', event=g.event_data)


@main.route('/action/<command>', methods=['GET'])
def action(command):
    '''
    action endpoint, supported commands:
        update - updates the json data file
    '''
    if command == "update":
        auth_token = current_app.config["AUTH_TOKEN"]
        if not auth_token:
            flash("AUTH_TOKEN not set")
            return redirect(url_for('main.matches'))

        headers = {"X-Auth-Token": auth_token}
        url = "http://api.football-data.org/v2/competitions/2018/matches"
        req = urllib.request.Request(url, None, headers)
        the_data = "{}"
        with urllib.request.urlopen(req) as response:
            the_data = response.read()

        fname = current_app.config["JSON_DATA_FILENAME"]
        f = open(fname, "w")
        f.write(the_data.decode("utf-8"))
        f.close()

        return redirect(url_for('main.matches'))

    flash("Unknown command given: {}".format(command))
    abort(404)


@main.route('/submitScore', methods=['POST'])
def submitScore():
    error = None
    if request.method == 'POST' and g.user:
        bet_string = request.form.get('bet')
        result_string = request.form.get('result')
        match_id = request.form.get('match_id')

        if result_string and g.user.has_write_permission():
            match = Match.query.filter_by(id=match_id).first()
            match.result = result_string
            db.session.commit()
            return "Ok"

        if not bet_string:
            error = "Invalid bet string"
        elif not match_id:
            error = "Invalid match_id"

        if error is None:
            print("received bet {} submit for match {}".format(bet_string,
                                                               match_id))

            bet = Bet.query.filter_by(user_id=g.user.id, match_id=match_id) \
                     .first()
            if bet:
                bet.bet = bet_string
                db.session.commit()
            else:
                bet = Bet(bet=bet_string, user=g.user, match_id=match_id)
                db.session.add(bet)
                db.session.commit()

            return "Ok"

    flash(error)
    return "Not Ok"


@main.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            return redirect(url_for('main.event'))
        else:
            error = 'Invalid username/password'

    if error:
        flash(error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html')


@main.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('main.event'))


@main.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'E-Mail is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            role = Role.query.filter_by(name='Tipper').first()
            user = User(username=username, password=password, email=email,
                        role=role)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))

        flash(error)

    return render_template('register.html')
