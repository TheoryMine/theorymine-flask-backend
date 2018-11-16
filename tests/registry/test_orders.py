import time
import uuid

def register_new_user(client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'helloBrenda1!'
    }
    registration_response = client.post('/auth/users', json=new_user)
    auth_token = registration_response.json['auth_token']
    return auth_token


def test_post_to_orders_success(db, client):
    auth_token = register_new_user(client)

    new_order = {
        'theorem_name': 'Brenda Theorem',
    }
    api_response = client.post('/registry/orders',
                               json=new_order,
                               headers={'Authorization': 'Bearer ' + auth_token})

    assert api_response.status_code == 201
    assert api_response.content_type == 'application/json'
    theorem_id = api_response.json['theorem_id']
    assert theorem_id is not None


def test_unauthorised_with_no_token(client):
    new_order = {'theorem_name': 'Brenda Theorem', }
    api_response = client.post('/registry/orders', json=new_order)
    assert api_response.status_code == 401


def test_unauthorised_with_expired_token(client):
    auth_token = register_new_user(client)
    time.sleep(1)

    new_order = {'theorem_name': 'Brenda Theorem', }
    api_response = client.post('/registry/orders',
                               json=new_order,
                               headers={'Authorization': 'Bearer ' + auth_token})
    assert api_response.status_code == 401
