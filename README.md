# Saarthi Backend - Smart Tourist Safety System

A FastAPI-based backend for the Saarthi tourist safety application.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Installation

1. **Clone and navigate to the backend directory**
   ```bash
   cd TOURIST-GUIDE-BACKEND
   ```

2. **Set up environment variables**
   ```bash
   # Create a .env file or set environment variables
   export DATABASE_URL="postgresql://username:password@localhost:5432/saarthi_db"
   ```

3. **Run the setup script**
   ```bash
   python setup.py
   ```

4. **Start the server**
   ```bash
   python setup.py start
   # OR
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### API Documentation

Once the server is running, visit:
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## 📊 Database Schema

### Tables
- `users` - Base user authentication
- `tourist_profiles` - Tourist-specific information
- `authority_profiles` - Authority/police profiles
- `incidents` - Reported incidents
- `alerts` - Alerts sent to tourists

## 🔗 API Endpoints

### Authentication (`/api/auth/`)
- `POST /register/tourist` - Register new tourist
- `POST /register/authority` - Register new authority
- `POST /login` - User login

### Tourist (`/api/tourist/`)
- `GET /profile/{user_id}` - Get tourist profile
- `POST /incidents` - Report incident
- `GET /incidents/{tourist_id}` - Get tourist's incidents
- `GET /alerts/{tourist_id}` - Get tourist's alerts
- `PUT /safety-score/{tourist_id}` - Update safety score

### Authority (`/api/authority/`)
- `GET /profile/{user_id}` - Get authority profile
- `GET /incidents` - Get all incidents
- `GET /incidents/status/{status}` - Get incidents by status
- `PUT /incidents/{incident_id}/status` - Update incident status
- `PUT /incidents/{incident_id}/priority` - Update incident priority
- `GET /alerts` - Get all alerts
- `GET /statistics/tourists` - Get tourist statistics

## 🛠️ Development

### Project Structure
```
app/
├── __init__.py
├── main.py              # FastAPI app and CORS setup
├── database.py          # Database connection
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── utils.py             # Utility functions
└── routes/
    ├── __init__.py
    ├── auth.py          # Authentication routes
    ├── tourist.py       # Tourist-specific routes
    └── authority.py     # Authority-specific routes
```

### Adding New Features
1. Add models to `models.py`
2. Add schemas to `schemas.py`
3. Create routes in appropriate route file
4. Update `main.py` to include new routes

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens (future use)
- `JWT_ALGORITHM` - JWT algorithm (future use)

### CORS Configuration
The app is configured to allow CORS from:
- http://localhost:3000
- http://localhost:19006
- http://127.0.0.1:19006
- http://127.0.0.1:3000

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL format
   - Verify database exists

2. **Port Already in Use**
   - Change port: `uvicorn app.main:app --reload --port 8001`
   - Kill existing process using port 8000

3. **Import Errors**
   - Ensure you're in the correct directory
   - Check Python path
   - Reinstall dependencies

## 📝 API Usage Examples

### Register a Tourist
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register/tourist" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tourist@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "document_type": "Passport",
    "document_number": "A1234567",
    "nationality": "American",
    "trip_start": "2024-01-01",
    "trip_end": "2024-01-15",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+1234567890"
  }'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tourist@example.com",
    "password": "password123"
  }'
```

### Report Incident
```bash
curl -X POST "http://127.0.0.1:8000/api/tourist/incidents?tourist_id=USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Theft Report",
    "description": "My wallet was stolen",
    "category": "Theft",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Smart India Hackathon 2025.