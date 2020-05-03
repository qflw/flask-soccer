# create virtual env
```bash
$ python -m venv venv
```

# activate virtual env
```bash
$ . venv/bin/activate
```

# run tests
```bash
$ python -m pytest tests/
or
pip install '.[test]'
pytest
or
pip install -e .
pytest
```

# run coverage
```bash
$ coverage run -m pytest
$ coverage report
$ coverage html  # open htmlcov/index.html in a browser
```

```python
import unittest

tests = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(tests)
```

# outer join example sql
```sql
sqlite> SELECT * from match left outer join bet on match.id = bet.match_id left outer join user on bet.user_id = user.id;
```


# run in dev mode

```bash
$ export FLASK_APP=soccer
$ export FLASK_ENV=development
$ flask run
```

# create secret key
```bash
$ python -c 'import os; print(os.urandom(16))'
```

# init db
```bash
$ flask init-db
```

# qeury matches for European Championship
curl -H "X-Auth-Token: 03e78b6da9344b42a295baf7b13a0035" http://api.football-data.org/v2/competitions/2018/matches
flask parse-json docs/2018_matches.json