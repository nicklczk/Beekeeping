# Beekeeping

Beekeeping is a serivce for beekeepers to keep track of their hives. It feature a login page, a schedule, and data entry. It will enable beekeepers to keep better track of, and have a central location to store information about the health of their bees.

## Requirements

- [Python 3.7](https://www.python.org) or Python 3.6
- [Pipenv](https://docs.pipenv.org)
- [npm](https://www.npmjs.com/get-npm)
- [Postgres](https://www.postgresql.org)

### Installing

```
git clone git@github.com:nicklczk/Beekeeping.git
cd Beekeeping
pipenv install
npm install
brew install postgresql
brew services start postgresql
createdb beekeeping
```

### Running 

``
pipenv shell
python manage.py createmigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Then go to localhost:8000

### Formatting

Please format your code with [Black](https://github.com/ambv/black) and use [Flake8](http://flake8.pycqa.org/en/latest/). Formatting will be enforced in order for a pull request to pass Travis CI test cases. 

### Considerations when creating Postgresql database

Depending on your system you may need to configure a Postgresql server if psycopg2 doesnt function correctly. If you createdb beekeeping, make migrations, and migrate and it still does not work you need to follow these instructions for createing a postgres server in the terminal:
- psql
- CREATE DATABASE beekeeping;
- CREATE USER beekeepinguser WITH PASSWORD '12345';
- ALTER ROLE beekeepinguser SET client_encodin g TO 'utf8';
- ALTER ROLE beekeepinguser SET default_transaction_isolation TO 'read committed';
- ALTER ROLE beekeepinguser SET timezone TO 'UTC';
- GRANT ALL PRIVILEGES ON DATABASE beekeeping TO beekeepinguser;
- \q
