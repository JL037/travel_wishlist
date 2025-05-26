## WishlistLocation
-id **PK**
-name
-description
-added_on
-visited

## VisitedLocation
-id **PK**
-wishlist_id **FK** -> WishlistLocation.id
-visited_on
-ratings
-notes
<!-- WishlistLocation 1️⃣ → 🔁 VisitedLocation -->


## User 
-id **PK**
-email
-hashed_password
-created_at
-role