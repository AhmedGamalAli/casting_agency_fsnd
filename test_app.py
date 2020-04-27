import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlluRXhLc19Sa09TQy0xby1RYy1TSCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZy1hZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM0YzI2NjNmODAwMGM4YzIyYTZkOSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg4MDExNTk5LCJleHAiOjE1ODgwMTg3OTksImF6cCI6IlowNEFVc3MwUFhMN0Vxcm9WRHF0QmFTVUJVcW41WHpLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.dkFuL2xUqUAf0uzh6O0SgerAVOYWpdT88VvnXJrMYbSsxNjfz16kFW4al5z73GoCztz1y0KqdHwM0MG9n0TbGJgKVQvS5VTB_2HPyd0GTyPln1nFitXSxib6Bn2t_580NDmVs9JgfYmVyz7cYyfs9lS3QYePqoza2ksuTWfJt78jmhO-sl153ClM1ICA_20g3PLH5W7NZT7zQyvNzz4skCwgA4GFf4L1mzAwPzkNZ9QWCLSCii0_Wxm6L9BzIXL--eLHOmz_od1jYaeCY7Xd_g9Pbqrb7t8eoO6OIJAYcI3bMHOt2uZNA49kwjruQXY_w2F5jkwyAO4_iyri1h3PIw'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlluRXhLc19Sa09TQy0xby1RYy1TSCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZy1hZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM0Yzk3NjNmODAwMGM4YzIyYTdjYSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg4MDExNzI3LCJleHAiOjE1ODgwMTg5MjcsImF6cCI6IlowNEFVc3MwUFhMN0Vxcm9WRHF0QmFTVUJVcW41WHpLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJtb2RpZnk6YWN0b3JzIiwibW9kaWZ5Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.bTF-C0Xtvts68aScKoQ7LbidRNuZQxRwpDNcDrGkXDkxkYiechN33l4w6UjBnex7ATfGOkIbK3uvmTaOG25Y2Z9uh7_egxyzGcT8J3LLEpcIZvT5_-5GcR4YfyfQ8ukijCLloayEO3pVtWhCX1MoxEfzOPwpY5GesYn7Hh4TemAyKRlUJt3MGNpCZlCRld_BYuCiVRMmh4Ripq1CPXB59ZGR1MRDukzUffvgVxJtYA1GPmSATR4oZ0gDyu21uwaaOSaR0x3sHyb8n2Iyd9ZoTDwtXY6u_1ucs5OWyRrz5NWWsEIOB2MDmk_2rQhqKJhHy2HkzMjQyOAMaZzjo2awJw'
executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlluRXhLc19Sa09TQy0xby1RYy1TSCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZy1hZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM0ZTZmNDlmYjI0MGM4YTI0ZTBiNyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg4MDExODA2LCJleHAiOjE1ODgwMTkwMDYsImF6cCI6IlowNEFVc3MwUFhMN0Vxcm9WRHF0QmFTVUJVcW41WHpLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJtb2RpZnk6YWN0b3JzIiwibW9kaWZ5Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.kVBYmrs888a_15SbmRXnkQqgevYejM8Owff5Q4l0uDgup6we7ptcmrD6MZcGiqB2muVny_GopqLdKKTKkRi4G_Cy75-tLHKDL_I-uou_dIWlgDsDFCAAyg5UDfPFHOZPjnA6aGV6Hc36kC9Dq20d5uLeZaIqOM-cHacTvcXQaZ2WhA-Pi8JurWIaSMAFh6W32GW3ZHMKL4mD0fv8QbEXrfSh0Qbccsx_kYPKj_S7TTZMKfSV4c0sXTx0A6abZY-I8Y1o9PfZ6Up20n7vlWvgdqm3Z0314eAra8bRegT_BJBhn0rIGsNuqrAEShVoDfBNR-dJTnpbYSfXMAIuY5S7Vw'


def set_auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(casting_assistant_token)}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(casting_director_token)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(executive_producer_token)}


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting_test'
        self.database_path = 'postgres://{}:{}@{}/{}'.format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'Bad Boys',
            'release_date': '1995-04-07'
        }

        self.new_actor = {
            'name': 'Ahmed Zaki',
            'age': 55,
            'gender': 'Male'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_movies(self):
        response = self.client().get('/movies', headers=set_auth_header('assistant'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_wrong_endpoint(self):
        response = self.client().get('/movie', headers=set_auth_header('assistant'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies_unauthorized(self):
        response = self.client().get('/movies', headers=set_auth_header(''))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is missing')

    def test_get_actors(self):
        response = self.client().get('/actors', headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_wrong_endpoint(self):
        response = self.client().get('/actor', headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_new_actor(self):
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])

    def test_post_new_actor_empty_body(self):
        response = self.client().post(
            '/actors', headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    def test_post_new_actor_unauthorized(self):
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=set_auth_header('assistant'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

    def test_post_new_movie(self):
        response = self.client().post('/movies', json=self.new_movie,
                                      headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])

    def test_post_new_movie_empty_body(self):
        response = self.client().post(
            '/movies', headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    def test_post_new_movie_unauthorized(self):
        response = self.client().post('/movies', json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

    def test_delete_movie(self):
        response = self.client().delete('/movies/1', headers=set_auth_header('producer'))
        data = json.loads(response.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_delete_movie_doesnt_exist(self):
        response = self.client().delete(
            '/movies/10000', headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_movie_unauthorized(self):
        response = self.client().delete('/movies/1', headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_delete_actor(self):
        response = self.client().delete('/actors/1', headers=set_auth_header('producer'))
        data = json.loads(response.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_delete_actor_doesnt_exist(self):
        response = self.client().delete(
            '/actors/10000', headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actor_unauthorized(self):
        response = self.client().delete('/actors/1', headers=set_auth_header('assistant'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/2',
            json=self.new_movie,
            headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_doesnt_exist(self):
        response = self.client().patch(
            '/movies/2000',
            json=self.new_movie,
            headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'bad request')

    def test_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/2',
            json=self.new_movie,
            headers=set_auth_header(''))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Authorization header is missing')

    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/2',
            json=self.new_actor,
            headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_doesnt_exist(self):
        response = self.client().patch(
            '/actors/2000',
            json=self.new_actor,
            headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'bad request')


if __name__ == "__main__":
    unittest.main()
