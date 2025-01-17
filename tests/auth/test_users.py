import hashlib
import uuid

def get_user_from_db(db, user_id):
    transaction = db.cursor()
    select_query = "SELECT id, firstname, lastname, email, password, userkind  FROM tm_users WHERE id = %s "
    transaction.execute(select_query, (user_id,))
    results = transaction.fetchall()
    return results

def get_all_users_from_db(db):
    transaction = db.cursor()
    select_query = "SELECT id, firstname, lastname, email, password, userkind  FROM tm_users "
    transaction.execute(select_query,)
    results = transaction.fetchall()
    return results

def test_post_to_users_success(db, client):
    email = 'brenda+{}@example.com'.format(str(uuid.uuid4()))
    password = 'helloBrenda1!'
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': email,
        'password': password
    }
    api_response = client.post('/auth/users', json=new_user)
    assert api_response.status_code == 201
    assert api_response.content_type == 'application/json'
    user_id = api_response.json['user_id']
    auth_token=api_response.json['auth_token']
    assert user_id is not None
    assert auth_token is not None

    user_values = get_user_from_db(db, user_id)
    assert len(user_values) == 1

    assert user_values[0]['firstname'] == new_user['first_name']
    assert user_values[0]['lastname'] == new_user['last_name']
    assert user_values[0]['email'] == new_user['email']
    assert user_values[0]['password'] == hashlib.md5('{}.{}'.format(email, password).encode()).hexdigest()

def test_post_to_users_with_missing_data_1(db, client):
    api_response = client.post('/auth/users')
    assert api_response.status_code == 400
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 0

def test_post_to_users_with_missing_data_2(db, client):
    new_user = {
        'first_name': 'Brenda',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'helloBrenda1!'
    }
    api_response = client.post('/auth/users', json=new_user)
    assert api_response.status_code == 400
    assert api_response.content_type == 'application/json'
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 0

def test_post_to_users_with_bad_email(db, client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brendaexample.com',
        'password': 'helloBrenda1!'
    }
    api_response = client.post('/auth/users', json=new_user)
    assert api_response.status_code == 400
    assert api_response.content_type == 'application/json'
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 0

def test_post_to_users_with_existing_email(db, client):
    email = 'brenda+{}@example.com'.format(str(uuid.uuid4()))
    fist_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': email,
        'password': 'helloBrenda1!'
    }
    second_user = {
        'first_name': 'Hello',
        'last_name': 'Moto',
        'email': email,
        'password': 'helloMoto1!'
    }
    client.post('/auth/users', json=fist_user)
    api_response = client.post('/auth/users', json=second_user)
    assert api_response.status_code == 400
    assert api_response.content_type == 'application/json'
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 1

def test_post_to_users_with_bad_password1(db, client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'a1'
    }
    api_response = client.post('/auth/users', json=new_user)
    assert api_response.status_code == 400
    assert api_response.content_type == 'application/json'
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 0

def test_post_to_users_with_bad_password2(db, client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'abcdefghi'
    }
    api_response = client.post('/auth/users', json=new_user)
    assert api_response.status_code == 400
    assert api_response.content_type == 'application/json'
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 0

def test_post_to_users_with_bad_password3(db, client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': '12345678'
    }
    api_response = client.post('/auth/users', json=new_user)
    assert api_response.status_code == 400
    assert api_response.content_type == 'application/json'
    all_users = get_all_users_from_db(db)
    assert len(all_users) == 0

