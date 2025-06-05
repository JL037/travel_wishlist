# import pytest
# from starlette.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from app.main import app
# from app.database import Base, get_db
# from app.core.config import settings

# TEST_DATABASE_URL = settings.TEST_DATABASE_URL

# # Create async engine + session
# engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
# TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# # Override get_db to use AsyncSession
# async def override_get_db():
#     async with TestingSessionLocal() as db:
#         yield db

# app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture(scope="function")
# def client():
#     # Drop and recreate tables before each test
#     import asyncio

#     async def _reset_db():
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.drop_all)
#             await conn.run_sync(Base.metadata.create_all)

#     asyncio.run(_reset_db())  # Run the async reset synchronously here

#     # Return the TestClient
#     with TestClient(app) as c:
#         yield c
