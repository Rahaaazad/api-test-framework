import pytest
from api_framework.models import User

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(client, user_id):
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200

    data = r.json()

    # Validate against schema
    user = User(**data)

    assert user.id == user_id
