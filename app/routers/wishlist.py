from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.services import wishlist_services
from app.crud import create_wishlist_item
from app.schema import locations

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist Items"]
)

@router.post("/", response_model=locations.WishlistLocationOut)
def create_wishlist_item(item: locations.WishlistLocationCreate, db: Session = Depends(get_db)):
    return crud.create_wishlist_item(db=db, item=item)

@router.get("/", response_model=list[locations.WishlistLocationOut])
def read_wishlist_items(db: Session = Depends(get_db)):
    return wishlist_services.get_all_items(db)