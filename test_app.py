import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlluRXhLc19Sa09TQy0xby1RYy1TSCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZy1hZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM0YzI2NjNmODAwMGM4YzIyYTZkOSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg3OTg0NTIyLCJleHAiOjE1ODc5OTE3MjIsImF6cCI6IlowNEFVc3MwUFhMN0Vxcm9WRHF0QmFTVUJVcW41WHpLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.bTJFNV0eEf3o570mo-g7TXcjnzs14Bcqoey3KgM3iqeXu68uokzGpjL_3_XFgbPBp3daIiRYzmuCsZ5ACQehPHDcdZTfLQSbK8c2PFZxg6C09s0IZ8DQLAbB5ZC4hTEHt2nJL4nW-CXq8zYM-f5IEV_nIQSHmaapMqsenpsyumaCuKottyCfu2hehC7OP8F86vonKOaP0o9BVsYjE_rUjU1R725i41xAsAbJVauSSpkJxf43E-LNzOw2svz3TGqfPU6pplHsC7iw46ZN2DyDF5dlxl-9WdKTMsUj6PIKkEUG9Ub0Qic7YtSP2mR5JL7IB_Da2aNS_zfCnp9qiaf_sw'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlluRXhLc19Sa09TQy0xby1RYy1TSCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZy1hZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM0Yzk3NjNmODAwMGM4YzIyYTdjYSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg3OTg0NjE5LCJleHAiOjE1ODc5OTE4MTksImF6cCI6IlowNEFVc3MwUFhMN0Vxcm9WRHF0QmFTVUJVcW41WHpLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJtb2RpZnk6YWN0b3JzIiwibW9kaWZ5Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.cWMYJIdgYjPZZAFvnElOtgNtu_9iskPeKNOp3Axh0-IoSocpV0j8y2JXnnnJtvCobjny9jWrLGSWbQpT3S9YBpYo8K2g0ZOfZVKXD8px7OVAChvCzmr6ZqBqMYi1F3H_gyfIgM7nd5CZpVBbbGbFaH_hJCtecxibjjiDIi386rdTdsOAr4pdo1ubpat8pj5fHVBn-zrcRT5zaf5avCVNR2v2HxUisPPqEr_IyqvdDRYdM86Ec-tscDf5sVD8YG-kF3czp6prex7fwePibdwmLkrMj4lrwvBQ6kZfoOQe3iTD2OZQJACec3qMfrZvPASDjKKuefkppNdErLA9iduW1Q'
executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlluRXhLc19Sa09TQy0xby1RYy1TSCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZy1hZ2VuY3kuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM0ZTZmNDlmYjI0MGM4YTI0ZTBiNyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg3OTg0Njk1LCJleHAiOjE1ODc5OTE4OTUsImF6cCI6IlowNEFVc3MwUFhMN0Vxcm9WRHF0QmFTVUJVcW41WHpLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJtb2RpZnk6YWN0b3JzIiwibW9kaWZ5Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.pXC1ndn_IkDCvUVXdDEYf0enGUvVVygDnMp4iy5W_SF2pEmDK3mUuKzC7MQuPoVQ9r19XKWr0qhH_J7hZm4vaI6hsXxCX5_RnLf9grq8kn9jdUspjVEyJJbF17UUsJhXlT0XdMuit5OU6v9L9bstEbz-KwMhNBbZ4NB3oKuK2wJPFEaTK1325FmBez72wBWnMPk-kCTIkKgrl6mPWFVhX05f08MpbloBGk9AyIowJl8Skl5b7L28FQjqUx4PhohwuQ6EqK-IrwdX8Rxr4ZDV6UcRGvHShXztmvKlBtdkEAzFyjM97kXxl3pbyhElAWrH9u2_qBPzyqOIe_TIjpL7vw'


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
            '/actors', json={}, headers=set_auth_header('director'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

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
            '/movies', json={}, headers=set_auth_header('producer'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'uprocessable')

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
