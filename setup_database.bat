@echo off
echo 🗄️ Setting up Saarthi Database
echo ================================

echo.
echo 📋 Database Setup Instructions:
echo.
echo 1. Make sure PostgreSQL is installed and running
echo 2. Open pgAdmin or command line
echo 3. Create a new database named 'saarthi_db'
echo 4. Set the DATABASE_URL environment variable
echo.
echo Example commands:
echo.
echo psql -U postgres
echo CREATE DATABASE saarthi_db;
echo \q
echo.
echo set DATABASE_URL=postgresql://postgres:your_password@localhost:5432/saarthi_db
echo.
echo Press any key after setting up the database...
pause > nul

echo.
echo 🚀 Testing database connection...
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL')
if db_url:
    print('✅ DATABASE_URL is set:', db_url)
else:
    print('❌ DATABASE_URL not found. Please set it.')
    print('Example: set DATABASE_URL=postgresql://postgres:password@localhost:5432/saarthi_db')
"

echo.
echo Press any key to continue...
pause > nul
