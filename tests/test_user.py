def test_read_user_with_token(client, valid_auth_token):
    response = client.get(
        "api/v1/user",
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "test@dev.com"
