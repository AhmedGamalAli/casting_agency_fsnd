# Casting Agency Capstone

This is a capstone project made for Udacity Full Stack Nanodegree
It is hosted on heroku. You can access it through this link.
https://capstone-fsnd-casting-agency.herokuapp.com/

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server
Each time you open a new terminal session, run (if you want to test the application locally):

```bash
export FLASK_APP=app.py;
```
To run the server, execute:
```bash
flask run
```
## Getting Started
## Authentcatied Users

AUTH0_DOMAIN = fsnd-casting-agency.auth0.com
API_AUDIENCE = casting-agency

We have three roles with different permissions in order to access it.
- Casting Assistant e-mail: casting_assistant@fsnd.com
                    password: capstone010*

- Casting Director e-mail: casting_director@fsnd.com
                   password: capstone010*

- Executive Producer e-mail: executive_producer@fsnd.com
                    password: capstone010*


## ENDPOINTS

- GET /movies:
View all the movies in the database, can be used by the 3 roles.

- GET /actors:
View all the actors in the database, can be used by the 3 roles.

- POST /actors:
Add new actor to the database, can be used only by casting director and executive producer.

- POST /movies:
Add new movies to the database, can be used only by executive producer.

- PATCH /actors/<int:actor_id>:
Modify actor data in the database, can be used only by casting director and executive producer.

- PATCH /movies/<int:movies_id>:
Modify movie data in the database, can be used only by casting director and executive producer.

- DELETE /actors/<int:actor_id>:
Delete actor from the database, can be used only by casting director and executive producer.

- DELETE /movies/<int:movie_id>:
Delete movie from database, can be used only by and executive producer.


## TEST

In you terminal run:

- python test_app.py