from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.services import wishlist_services
from app.crud import create_wishlist_item

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist Items"]
)

@router.post("/", response_model=schemas.WishlistItemOut)
def create_wishlist_item(item: schemas.WishlistItemCreate, db: Session = Depends(get_db)):
    return crud.create_wishlist_item(db=db, item=item)

@router.get("/", response_model=list[schemas.WishlistItemOut])
def read_wishlist_items(db: Session = Depends(get_db)):
    return wishlist_services.get_all_items(db)