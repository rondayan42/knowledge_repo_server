"""
Seed Root User for Knowledge Repository - SQLAlchemy version
Creates or updates the root admin user
"""

import os
import sys

# Add server directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from database import init_db, get_db
from models.orm import User
from auth import hash_password

ROOT_EMAIL = 'rondayan42@gmail.com'
ROOT_PASSWORD = os.getenv('ROOT_INITIAL_PASSWORD', 'BsmartRoot2025!')


def seed_default_data():
    """Seed default categories, departments, and priorities."""
    from models.orm import Category, Department, Priority
    
    db = get_db()
    try:
        # Default categories
        categories = [
            ('הדרכה', 'מאמרי הדרכה והכשרה'),
            ('נהלים', 'נהלי עבודה ותקנון'),
            ('טכני', 'מידע טכני ותמיכה'),
            ('שירות לקוחות', 'מידע לנציגי שירות'),
            ('מכירות', 'חומרי מכירות ומידע מסחרי'),
            ('כללי', 'מידע כללי')
        ]
        for name, desc in categories:
            existing = db.query(Category).filter_by(name=name).first()
            if not existing:
                db.add(Category(name=name, description=desc))
        
        # Default departments
        departments = [
            ('תפעול', 'מחלקת תפעול'),
            ('פיתוח', 'מחלקת פיתוח תוכנה'),
            ('שיווק', 'מחלקת שיווק ופרסום'),
            ('משאבי אנוש', 'מחלקת משאבי אנוש'),
            ('הנהלה', 'הנהלת החברה'),
            ('תמיכה טכנית', 'מחלקת תמיכה טכנית')
        ]
        for name, desc in departments:
            existing = db.query(Department).filter_by(name=name).first()
            if not existing:
                db.add(Department(name=name, description=desc))
        
        # Default priorities
        priorities = [
            ('דחוף', 4, '#DC3545'),
            ('גבוהה', 3, '#E74C5C'),
            ('בינונית', 2, '#FFC107'),
            ('נמוכה', 1, '#28A745')
        ]
        for name, level, color in priorities:
            existing = db.query(Priority).filter_by(name=name).first()
            if not existing:
                db.add(Priority(name=name, level=level, color=color))
        
        db.commit()
        print('✅ Default data seeded successfully')
        
    except Exception as e:
        db.rollback()
        print(f'Error seeding data: {e}')
    finally:
        db.close()


def seed_root_user():
    print(f'Checking for root user: {ROOT_EMAIL}...')
    
    try:
        # Initialize database first
        init_db()
        seed_default_data()
        
        db = get_db()
        try:
            # Check if root user exists
            user = db.query(User).filter_by(email=ROOT_EMAIL).first()
            
            if user:
                print('Root user already exists.')
                # Ensure admin privileges
                user.role = 'admin'
                user.approved = True
                user.is_root = True
                db.commit()
                print('Root user privileges confirmed.')
            else:
                print('Root user not found. Creating...')
                password_hash = hash_password(ROOT_PASSWORD)
                
                user = User(
                    email=ROOT_EMAIL,
                    password_hash=password_hash,
                    role='admin',
                    approved=True,
                    is_root=True
                )
                db.add(user)
                db.commit()
                
                print(f'Root user created successfully.')
                print(f'Email: {ROOT_EMAIL}')
                print(f'Password: {ROOT_PASSWORD}')
                print('IMPORTANT: Change the default password after first login.')
        finally:
            db.close()
        
    except Exception as e:
        print(f'Error seeding root user: {e}')
        sys.exit(1)


if __name__ == '__main__':
    seed_root_user()
