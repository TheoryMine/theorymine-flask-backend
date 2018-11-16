import pytest
from flask import jsonify
import uuid
import time

from app.auth.authorization import auth_token_required
from app.exceptions import UnauthorisedError


def get_user_from_db(db, user_id):
    transaction = db.cursor()
    select_query = "SELECT id, firstname, lastname, email, password, userkind  FROM tm_users WHERE id = %s "
    transaction.execute(select_query, (user_id,))
    results = transaction.fetchall()
    return results


def test_auth_token_provided_successfully(app, client, db):

    @app.route('/fake')
    @auth_token_required
    def fake(user_id):
        resp = jsonify({'message': 'this is fake!', 'user_id': user_id})
        resp.status_code = 200
        return resp

    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'helloBrenda1!'
    }
    registration_response = client.post('/auth/users', json=new_user)
    auth_token = registration_response.json['auth_token']
    api_response = client.get('/fake',  headers={'Authorization':'Bearer ' + auth_token})

    assert api_response.status_code == 200
    assert api_response.json['message'] == 'this is fake!'

    user_id = api_response.json['user_id']
    assert user_id is not None
    user_values = get_user_from_db(db, user_id)
    assert len(user_values) == 1

    assert user_values[0]['firstname'] == new_user['first_name']
    assert user_values[0]['lastname'] == new_user['last_name']
    assert user_values[0]['email'] == new_user['email']

def test_unauthorised_bad_token(app, client):

    @app.route('/fake')
    @auth_token_required
    def fake(user_id):
        resp = jsonify({'message': 'this is fake!'})
        resp.status_code = 200
        return resp
    response = client.get('/fake',  headers={'Authorization':'Bearer random-bad-token' })
    assert response.status_code == 401
    assert response.json['message']=="User unauthorised to make this request"


def test_unauthorised_no_token1(app, client):
    @app.route('/fake')
    @auth_token_required
    def fake(user_id):
        resp = jsonify({'message': 'this is fake!'})
        resp.status_code = 200
        return resp
    response = client.get('/fake',  headers={'Authorization': None })
    assert response.status_code == 401
    assert response.json['message']=='Please provide an auth token'


def test_unauthorised_no_token2(app, client):
    @app.route('/fake')
    @auth_token_required
    def fake(user_id):
        resp = jsonify({'message': 'this is fake!'})
        resp.status_code = 200
        return resp
    response = client.get('/fake',  headers={ })
    assert response.status_code == 401
    assert response.json['message']=='Please provide an auth token'


def test_unauthorised_no_expired(app, client):
    @app.route('/fake')
    @auth_token_required
    def fake(user_id):
        resp = jsonify({'message': 'this is fake!', 'user_id': user_id})
        resp.status_code = 200
        return resp

    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'helloBrenda1!'
    }
    registration_response = client.post('/auth/users', json=new_user)
    auth_token = registration_response.json['auth_token']
    time.sleep(1)
    response = client.get('/fake',  headers={'Authorization':'Bearer ' + auth_token})
    assert response.status_code == 401
    assert response.json['message']=='Signature expired. Please log in again'



