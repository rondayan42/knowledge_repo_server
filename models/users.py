"""
Users model for Knowledge Repository - SQLAlchemy version
"""

from datetime import datetime
from database import get_db
from models.orm import User


class Users:
    @staticmethod
    def get_by_email(email):
        db = get_db()
        try:
            user = db.query(User).filter_by(email=email).first()
            return user.to_dict(include_password=True) if user else None
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            user = db.query(User).filter_by(id=id).first()
            return user.to_dict() if user else None
        finally:
            db.close()
    
    @staticmethod
    def create(email, password_hash, role='user', approved=False):
        db = get_db()
        try:
            user = User(
                email=email,
                password_hash=password_hash,
                role=role,
                approved=approved
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def update_last_login(id):
        db = get_db()
        try:
            user = db.query(User).filter_by(id=id).first()
            if user:
                user.last_login_at = datetime.utcnow()
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def update_role(id, role):
        db = get_db()
        try:
            user = db.query(User).filter_by(id=id).first()
            if user:
                user.role = role
                db.commit()
                db.refresh(user)
                return user.to_dict()
            return None
        finally:
            db.close()
    
    @staticmethod
    def update_approved(id, approved):
        db = get_db()
        try:
            user = db.query(User).filter_by(id=id).first()
            if user:
                user.approved = approved
                db.commit()
                db.refresh(user)
                return user.to_dict()
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_all():
        db = get_db()
        try:
            users = db.query(User).order_by(User.created_at.desc()).all()
            return [u.to_dict() for u in users]
        finally:
            db.close()
    
    @staticmethod
    def delete(id):
        db = get_db()
        try:
            user = db.query(User).filter_by(id=id).first()
            if user and user.is_root:
                raise Exception('Cannot delete root user')
            if user:
                db.delete(user)
                db.commit()
            return True
        finally:
            db.close()
