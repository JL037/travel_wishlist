from fastapi import FastAPI
from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Any

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Travel Wishlist API!'}

def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()