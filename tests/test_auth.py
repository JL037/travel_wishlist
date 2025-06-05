import uuid
import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"  # Replace if your app runs on a different host/port


@pytest.mark.asyncio
async def test_create_and_login():
    email = f"pytest_{uuid.uuid4().hex[:6]}@example.com"

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Register
        register = await client.post(
            "/auth/register",
            json={"email": email, "username": "pytestuser", "password": "testpass"},
        )
        assert register.status_code == 201

        # Login
        login = await client.post(
        "/auth/login",
        data={"username": email, "password": "testpass"},  # no headers needed
        )
        assert login.status_code == 200
        assert "access_token" in login.json()





@pytest.mark.asyncio
async def test_access_protected_route():
    email = f"pytest_{uuid.uuid4().hex[:6]}@example.com"

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Register
        res = await client.post(
            "/auth/register",
            json={"email": email, "username": "pytestuser", "password": "testpass"},
        )
        assert res.status_code == 201

        # Login
        res = await client.post(
            "/auth/login",
            data={"username": email, "password": "testpass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 200
        token = res.json()["access_token"]

        # Use token in cookie
        client.cookies.set("access_token", token)

        # Access protected route
        response = await client.get("/wishlist/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_invalid_login():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        res = await client.post(
            "/auth/login",
            data={"username": "wrong@example.com", "password": "wrongpass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_no_cookie():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        res = await client.get("/wishlist/")
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_duplicate_registration():
    email = f"pytest_{uuid.uuid4().hex[:6]}@example.com"
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Register once
        res = await client.post(
            "/auth/register",
            json={"email": email, "username": "pytestuser", "password": "testpass"},
        )
        assert res.status_code == 201

        # Attempt duplicate registration
        res = await client.post(
            "/auth/register",
            json={"email": email, "username": "pytestuser", "password": "testpass"},
        )
        assert res.status_code in [400, 409]


@pytest.mark.asyncio
async def test_invalid_registration_payload():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Missing email
        res = await client.post("/auth/register", json={"username": "pytestuser", "password": "testpass"})
        assert res.status_code == 422

        # Missing password
        res = await client.post("/auth/register", json={"email": "pytest@example.com", "username": "pytestuser"})
        assert res.status_code == 422

        # Invalid email format
        res = await client.post(
            "/auth/register", json={"email": "not-an-email", "username": "pytestuser", "password": "testpass"}
        )
        assert res.status_code in [400, 422]


@pytest.mark.asyncio
async def test_fetch_profile():
    email = f"pytest_{uuid.uuid4().hex[:6]}@example.com"
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Register
        await client.post(
            "/auth/register",
            json={"email": email, "username": "pytestuser", "password": "testpass"},
        )

        # Login
        res = await client.post(
            "/auth/login",
            data={"username": email, "password": "testpass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert res.status_code == 200
        token = res.json()["access_token"]

        # Set cookie
        client.cookies.set("access_token", token)

        # Fetch profile
        res = await client.get("/auth/me")
        assert res.status_code == 200
        assert res.json()["email"] == email
