"""
Database initialization script.
Run this before starting the server to ensure tables exist and default data is seeded.
"""
from database import init_db
from app import seed_default_data

if __name__ == "__main__":
    print("🔄 Initializing database...")
    try:
        init_db()
        seed_default_data()
        print("✅ Database initialization complete.")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        exit(1)
