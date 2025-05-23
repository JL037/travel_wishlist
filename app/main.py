from fastapi import FastAPI
from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Any
from app.routers import wishlist

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Travel Wishlist API!'}

app.include_router(wishlist.router)
