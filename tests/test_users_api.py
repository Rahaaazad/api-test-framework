import pytest

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(client, user_id):
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == user_id
    assert "name" in data
    assert "email" in data
def test_get_user_not_found(client):
    r = client.get("/users/999999")
    assert r.status_code == 404
