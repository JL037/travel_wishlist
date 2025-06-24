import uuid


def test_create_and_login(client):
    # unique email to prevent collision
    email = f"pytest_{uuid.uuid4().hex[:6]}@example.com"

    # Register
    register = client.post(
        "/auth/register", json={"email": email, "password": "testpass", "role": "user"}
    )
    assert register.status_code == 201

    # Login
    login = client.post(
        "/auth/login",
        data={"username": email, "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()
   


def test_access_protected_route(client):
    # Step 1: Register
    register = client.post(
        "/auth/register",
        json={"email": "pytest2@example.com", "password": "testpass", "role": "user"},
    )
    assert register.status_code == 201

    # Step 2: Login
    login = client.post(
        "/auth/login",
        data={"username": "pytest2@example.com", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Step 3: Set cookie manually on client
    client.cookies.set("access_token", token)

    # Step 4: Try accessing a protected route
    response = client.get("/wishlist/")
    assert (
        response.status_code == 200 or response.status_code == 404
    )  # Adjust if list is empty


def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        data={"username": "wrong@example.com", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_protected_route_no_cookie(client):
    response = client.get("/wishlist/")
    assert response.status_code == 401
