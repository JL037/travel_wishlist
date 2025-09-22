# Travel Wishlist 🌍

A full-stack web application that helps you track your dream travel destinations, manage visited locations, plan trips, and check weather information for your future adventures.

![Travel Wishlist](frontend/public/map.jpg)

## ✨ Features

### 🎯 Core Features
- **Wishlist Management**: Add, edit, and organize places you want to visit
- **Visited Locations**: Track places you've been with notes and ratings
- **Interactive Map**: Visualize all your locations on a beautiful world map
- **Travel Planning**: Calendar-based trip planning with date management
- **Weather Integration**: Check current weather for any city worldwide
- **User Authentication**: Secure registration and login system

### 🔧 Technical Features
- **Real-time Updates**: Seamless data synchronization
- **Responsive Design**: Works perfectly on desktop and mobile
- **Geocoding**: Automatic coordinate lookup for locations
- **Tour Mode**: Demo version for new users to explore features
- **Password Reset**: Email-based password recovery system

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **JWT Authentication** - Secure token-based authentication
- **Asyncio** - Asynchronous programming support

### Frontend
- **React 18** - Modern UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Leaflet** - Interactive maps
- **React Big Calendar** - Calendar component for trip planning

### External APIs
- **OpenWeatherMap** - Weather data
- **Nominatim (OpenStreetMap)** - Geocoding services
- **Resend** - Email delivery service

### DevOps & Monitoring
- **Docker** - Containerization
- **Sentry** - Error tracking and performance monitoring
- **Alembic** - Database migrations
- **pytest** - Testing framework

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/travel-wishlist.git
   cd travel-wishlist
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Optional: Seed database
   python app/seeds/seed_db.py
   ```

6. **Start the backend**
   ```bash
   uvicorn app.main:app --reload
   # Or use the Makefile
   make run
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env.local
   # Edit with your API URL and other config
   ```

4. **Start the frontend**
   ```bash
   npm run dev
   ```

### Docker Setup (Alternative)

```bash
# Copy environment file
cp .env.example .env

# Start all services
docker-compose up --build
```

## 📁 Project Structure

```
travel-wishlist/
├── app/                          # Backend application
│   ├── core/                     # Core configuration
│   ├── models/                   # Database models
│   ├── routers/                  # API endpoints
│   ├── schema/                   # Pydantic schemas
│   ├── services/                 # Business logic
│   ├── utils/                    # Utility functions
│   └── main.py                   # FastAPI application
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   ├── pages/                # Page components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── api/                  # API client functions
│   │   └── App.tsx               # Main app component
│   └── public/                   # Static assets
├── migrations/                   # Database migrations
├── tests/                        # Test files
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Docker image definition
├── Makefile                      # Development commands
└── requirements.txt              # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/travel_wishlist
TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost/travel_wishlist_test

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
OPEN_WEATHER_API_KEY=your-openweather-api-key
RESEND_API_KEY=your-resend-api-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### Frontend Environment

Create a `.env.local` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
VITE_SENTRY_DSN=your-frontend-sentry-dsn
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /wishlist` - Get user's wishlist
- `POST /wishlist` - Add new wishlist item
- `GET /visited` - Get visited locations
- `GET /api/weather` - Get weather data
- `POST /api/travel-plans` - Create travel plan

## 🚀 Deployment

### Using Docker

```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f
```

### Manual Deployment

1. **Backend**: Deploy to platforms like Railway, Heroku, or DigitalOcean
2. **Frontend**: Deploy to Vercel, Netlify, or similar
3. **Database**: Use managed PostgreSQL service

### Production Considerations

- Set `DEBUG=False` in production
- Use environment-specific configuration
- Set up proper logging and monitoring
- Configure CORS for your frontend domain
- Use HTTPS in production
- Set up database backups

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all new frontend code
- Write tests for new features
- Update documentation as needed
- Run linting before committing:
  ```bash
  # Backend
  black .
  ruff check .
  
  # Frontend
  npm run lint
  ```

## 📝 Available Commands

### Backend (Makefile)
```bash
make run          # Start FastAPI server
make test         # Run tests
make secure       # Run security scans
make clean        # Remove cache files
make docker       # Start with Docker
make psql         # Connect to PostgreSQL
```

### Frontend
```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run preview   # Preview production build
npm run lint      # Run ESLint
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Run migrations: `alembic upgrade head`

2. **Frontend API Errors**
   - Verify VITE_API_URL points to backend
   - Check CORS configuration
   - Ensure backend is running

3. **Authentication Issues**
   - Clear browser cookies
   - Check JWT secret key configuration
   - Verify token expiration settings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [OpenStreetMap](https://www.openstreetmap.org/) for geocoding services
- [Leaflet](https://leafletjs.com/) for interactive maps
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework

## 📞 Support

- Create an [issue](https://github.com/yourusername/travel-wishlist/issues) for bug reports
- Start a [discussion](https://github.com/yourusername/travel-wishlist/discussions) for questions
- Check the [documentation](https://github.com/yourusername/travel-wishlist/wiki) for detailed guides

---

**Happy Traveling! 🌟**