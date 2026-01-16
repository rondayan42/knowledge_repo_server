"""
Categories model for Knowledge Repository - SQLAlchemy version
"""

from sqlalchemy import func
from database import get_db
from models.orm import Category, Article


class Categories:
    @staticmethod
    def get_all():
        db = get_db()
        try:
            categories = db.query(Category).order_by(Category.name).all()
            return [c.to_dict() for c in categories]
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            category = db.query(Category).filter_by(id=id).first()
            return category.to_dict() if category else None
        finally:
            db.close()
    
    @staticmethod
    def create(name, description=None, creator_id=None):
        db = get_db()
        try:
            category = Category(
                name=name,
                description=description,
                created_by=creator_id
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            return category.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def update(id, name, description=None):
        db = get_db()
        try:
            category = db.query(Category).filter_by(id=id).first()
            if category:
                category.name = name
                category.description = description
                db.commit()
                db.refresh(category)
                return category.to_dict()
            return None
        finally:
            db.close()
    
    @staticmethod
    def delete(id):
        db = get_db()
        try:
            category = db.query(Category).filter_by(id=id).first()
            if category:
                db.delete(category)
                db.commit()
            return True
        finally:
            db.close()
    
    @staticmethod
    def is_in_use(id):
        db = get_db()
        try:
            count = db.query(func.count(Article.id)).filter(Article.category_id == id).scalar()
            return count > 0
        finally:
            db.close()
