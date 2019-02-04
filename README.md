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
```

### Running 

```
pipenv shell
python app.py
```
Then go to localhost:8000

### Formatting

Please format your code with [Black](https://github.com/ambv/black) and use [Flake8](http://flake8.pycqa.org/en/latest/). Formatting will be enforced in order for a pull request to pass Travis CI test cases. 