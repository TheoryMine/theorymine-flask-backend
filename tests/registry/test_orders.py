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

def get_unique_key_from_db(db):
    transaction = db.cursor()
    select_query = "SELECT id FROM tm_unique_keys "
    transaction.execute(select_query)
    results = transaction.fetchone()
    return results

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

    history_id = get_unique_key_from_db(db)
    assert history_id is not None


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
