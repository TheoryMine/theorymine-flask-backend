def test_post_to_orders_success(db, client):
    new_order = {
        'theorem_name': 'Brenda Theorem',
    }
    api_response = client.post('/registry/orders', json=new_order)
    assert api_response.status_code == 201
    assert api_response.content_type == 'application/json'
    theorem_id = api_response.json['theorem_id']
    assert theorem_id is not None
