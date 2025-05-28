from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.services import wishlist_services
from app.schema import locations
from app.dependencies.auth import get_current_user
from app.models.location import WishlistLocation
from app.models.users import User

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist Items"]
)


@router.post("/", response_model=locations.WishlistLocationOut)
def create_wishlist_item(
    item: locations.WishlistLocationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud.create_wishlist_item(db=db, item=item, user_id=current_user.id)


@router.get("/", response_model=list[locations.WishlistLocationOut])
def read_wishlist_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(WishlistLocation).filter(
        WishlistLocation.owner_id == current_user.id
    ).all()

@router.get("/wishlist/{wishlist_id}", response_model=locations.WishlistLocationOut)
def read_location_by_id(wishlist_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    location = db.query(WishlistLocation).filter(WishlistLocation.id == wishlist_id, WishlistLocation.owner_id == current_user.id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return location

@router.patch("/wishlist/{wishlist_id}", response_model=locations.WishlistLocationOut)
def update_location(wishlist_id: int, location_data: locations.WishlistLocationUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    location = db.query(WishlistLocation).filter(WishlistLocation.id == wishlist_id, WishlistLocation.owner_id == current_user.id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    for field, value in location_data.model_dump(exclude_unset=True).items():
        print(f"🛠 Updating field {field} to value {value}")
        setattr(location, field, value)
    
    db.commit()
    db.refresh(location)
    return location

@router.delete("/wishlist/{wishlist_id}", status_code=204)
def delete_location(wishlist_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    location = db.query(WishlistLocation).filter(WishlistLocation.id == wishlist_id, WishlistLocation.owner_id == current_user.id).first()
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    
    db.delete(location)
    db.commit()
    return
