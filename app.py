import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, \
          Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, \
          POST, PUT, DELETE, OPTIONS')
        return response

    # ROUTES
    @app.route('/')
    def index():
        return "Welcome to our Casting Agency"

    @app.route('/movies')
    @requires_auth('view:movies')
    def get_movies(token):
        all_movies = Movie.query.all()

        if len(all_movies) == 0:
            abort(404)

        movies = [movie.format() for movie in all_movies]

        return jsonify({
            'success': True,
            'movies': movies
          })

    @app.route('/actors')
    @requires_auth('view:actors')
    def get_actors(token):
        all_actors = Actor.query.all()

        if len(all_actors) == 0:
            abort(404)

        actors = [actor.format() for actor in all_actors]

        return jsonify({
            'success': True,
            'actors': actors
          })

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def add_movie(token):
        body = request.get_json()

        if body is None:
            abort(400)

        new_movie_title = body.get('title', None)
        new_movie_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_movie_title, release_date=new_movie_release_date)
            movie.insert()

            total_movies = len(Movie.query.all())

            return jsonify({
                'success': True,
                'added': movie.id,
                'total_movies': total_movies
              })

        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def add_actor(token):
        body = request.get_json()

        if body is None:
            abort(400)

        new_actor_name = body.get('name', None)
        new_actor_age = body.get('age', None)
        new_actor_gender = body.get('gender', None)

        try:
            actor = Actor(name=new_actor_name, age=new_actor_age, gender=new_actor_gender)
            actor.insert()

            total_actors = len(Actor.query.all())

            return jsonify({
                'success': True,
                'added': actor.id,
                'total_actors': total_actors
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)
            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.id
                })

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)
            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor.id
                })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('modify:movies')
    def update_movie(token, movie_id):
        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)
            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            updated_movie = Movie.query.filter(Movie.id == movie_id).first()

            return jsonify({
                'success': True,
                'movies': updated_movie.format()
                })

        except:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('modify:actors')
    def update_actor(token, actor_id):
        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)
            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()
            updated_actor = Actor.query.filter(Actor.id == actor_id).first()

            return jsonify({
                'success': True,
                'actors': updated_actor.format()
                })

        except:
            abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
            }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
            }), e.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
