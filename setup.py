#!/usr/bin/env python3
"""
Setup script for Saarthi Backend
This script helps set up the database and run the application
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def setup_database():
    """Set up the database"""
    print("🗄️ Setting up database...")
    
    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        print("⚠️  DATABASE_URL not set. Please set it in your environment or .env file")
        print("   Example: export DATABASE_URL='postgresql://user:password@localhost:5432/saarthi_db'")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return run_command("pip install -r requirements.txt", "Installing dependencies")
    else:
        print("⚠️  No virtual environment detected. Creating one...")
        run_command("python -m venv venv", "Creating virtual environment")
        print("✅ Virtual environment created. Please run:")
        print("   Windows: activate_venv.bat")
        print("   Linux/Mac: source activate_venv.sh")
        return False

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    # Since we're using SQLAlchemy with create_all, migrations are automatic
    print("✅ Database tables will be created automatically on first run")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    print("   Server will be available at: http://127.0.0.1:8000")
    print("   API documentation at: http://127.0.0.1:8000/docs")
    print("   Press Ctrl+C to stop the server")
    
    return run_command("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000", "Starting server")

def main():
    """Main setup function"""
    print("🎯 Saarthi Backend Setup")
    print("=" * 50)
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        return
    
    # Run migrations
    run_migrations()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Make sure your PostgreSQL database is running")
    print("2. Set DATABASE_URL environment variable")
    print("3. Run: python setup.py start")
    print("4. Or run: uvicorn app.main:app --reload")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start_server()
    else:
        main()
