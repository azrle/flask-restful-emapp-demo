import json


def test_events_list(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    got = json.loads(response.data)
    assert len(got) == 2
    assert got[0]['id'] == 2 and got[1]['id'] == 1
    assert got[0]['name'] == 'bar' and got[1]['name'] == 'foo'
