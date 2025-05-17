# Travel Wishlist

### Description

Travel Wishlist is a web application that allows users to keep track of their dream travel destinations. Users can create, update, and manage a list of places they want to visit, mark destinations as visited, and explore additional details about each location.

### Tech Stack

* **Backend:** FastAPI
* **Frontend:** React or Next.js
* **Database:** PostgreSQL or SQLite
* **Optional Integrations:** Google Maps API, Weather API

### Features

* Add, update, and delete destinations
* Mark destinations as visited or unvisited
* View details for each destination
* Optional map view of all travel spots
* Optional weather information for each destination

### Project Structure

```
travel_wishlist/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
│
├── .env
├── requirements.txt
├── alembic.ini
└── README.md
```

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/travel_wishlist.git
   cd travel_wishlist
   ```

2. **Set up virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use .\venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   uvicorn app.main:app --reload
   ```

   Open [http://localhost:8000/docs](http://localhost:8000/docs) to view Swagger UI.

### Future Improvements

* Integration with Google Maps API
* Weather updates for each destination
* User authentication for personal travel lists

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

