# Backend - Movie Center

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt

pip install python-jose
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.


- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Set up the Database

You must go .env file and replace your config

With Postgres running, create a `movies` database:

```bash
createbd movies
```

Populate the database using the `movies.psql` file provided. From the `backend` folder in terminal run:

```bash
psql movies < movies.psql
```

Replace your password of Postgres in models.py

### Run the Server

<!-- From within the `./src` directory first ensure you are working using your created virtual environment. -->

I implement API in the app.py, so you should set up the FLASK_APP environment variable used to run the app.

- For CMD

```bash
set FLASK_APP=app.py

```

- For PowerShell

```bash
$env:FLASK_APP = "app"

```

To run the server, execute:

```bash

flask run --reload

```

The `--reload` flag will detect file changes and restart the server automatically.

### Setup Auth0

You must go .env file and replace your config

#### Log in account:
- mail: dahidev275@steamoh.com
- password: 123456789@Bnm

or 

#### Create a new Auth0 Account
1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:reviews-detail`
    - `post:movies`
    - `post:reviews`
    - `patch:movies`
    - `delete:movies`
    - `delete:reviews`
6. Create new roles for:
   - Customer
     - can `get:reviews-detail`
     - can `get:movies`
   - Manager
     - can perform all actions

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

You must go .env file and replace your config

To deploy the tests, run

```bash
dropdb movies_test
createdb movies_test
psql movies_test < movies.psql
python test_flaskr.py
```

## Link deploy
https://moviescenter123.herokuapp.com/