import json
from emapp.db import get_db


def get_signup(app, event_id, email):
    """
    Get a single event by its id.
    Return None if it's not found.
    """
    with app.app_context():
        db = get_db()
        return db.execute((
            'SELECT event_id, email '
            'FROM signup WHERE event_id=? AND email=?'),
            (event_id, email)).fetchone()


def test_signup_post(app, client):
    path = "/api/signup/events/1/email/foo@example.com"
    # not auth.
    response = client.post(path)
    assert response.status_code == 401
    # success.
    response = client.post(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 201
    assert response.headers["Location"] == (
        "http://localhost/api/signup/events/1")
    s = get_signup(app, 1, 'foo@example.com')
    assert s['event_id'] == 1
    assert s['email'] == 'foo@example.com'

    # duplicated.
    response = client.post(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 409
    # event not found.
    path = "/api/signup/events/3/email/foo@example.com"
    response = client.post(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 404


def test_signup_delete(app, client):
    path = "/api/signup/events/1/email/foo@example.com"
    # not auth.
    response = client.delete(path)
    assert response.status_code == 401
    # success.
    # insert first.
    response = client.post(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 201
    # then delete.
    response = client.delete(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 204
    s = get_signup(app, 1, 'foo@example.com')
    assert s is None
    # event not found.
    path = "/api/signup/events/3/email/foo@example.com"
    response = client.post(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 404


def test_signup_list(client):
    path = "/api/signup/events/2"
    # not auth.
    response = client.get(path)
    assert response.status_code == 401
    # success.
    # insert first.
    response = client.post(
        path + '/email/foo@example.com',
        headers={'x-simple-auth': "test"})
    assert response.status_code == 201
    response = client.post(
        path + '/email/bar@example.com',
        headers={'x-simple-auth': "test"})
    assert response.status_code == 201
    # then list.
    response = client.get(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 200
    got = json.loads(response.data)
    assert len(got) == 2
    assert got[0]['event_id'] == got[1]['event_id'] == 2
    assert got[0]['email'] == 'bar@example.com'
    assert got[1]['email'] == 'foo@example.com'
    # event not found.
    path = "/api/signup/events/3"
    response = client.get(
        path,
        headers={'x-simple-auth': "test"})
    assert response.status_code == 404
