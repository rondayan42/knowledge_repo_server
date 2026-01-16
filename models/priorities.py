"""
Priorities model for Knowledge Repository - SQLAlchemy version
"""

from sqlalchemy import func
from database import get_db
from models.orm import Priority, Article


class Priorities:
    @staticmethod
    def get_all():
        db = get_db()
        try:
            priorities = db.query(Priority).order_by(Priority.level.desc()).all()
            return [p.to_dict() for p in priorities]
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            priority = db.query(Priority).filter_by(id=id).first()
            return priority.to_dict() if priority else None
        finally:
            db.close()
    
    @staticmethod
    def create(name, level=0, color=None, creator_id=None):
        db = get_db()
        try:
            priority = Priority(
                name=name,
                level=level,
                color=color,
                created_by=creator_id
            )
            db.add(priority)
            db.commit()
            db.refresh(priority)
            return priority.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def update(id, name, level=None, color=None):
        db = get_db()
        try:
            priority = db.query(Priority).filter_by(id=id).first()
            if priority:
                priority.name = name
                if level is not None:
                    priority.level = level
                if color is not None:
                    priority.color = color
                db.commit()
                db.refresh(priority)
                return priority.to_dict()
            return None
        finally:
            db.close()
    
    @staticmethod
    def delete(id):
        db = get_db()
        try:
            priority = db.query(Priority).filter_by(id=id).first()
            if priority:
                db.delete(priority)
                db.commit()
            return True
        finally:
            db.close()
    
    @staticmethod
    def is_in_use(id):
        db = get_db()
        try:
            count = db.query(func.count(Article.id)).filter(Article.priority_id == id).scalar()
            return count > 0
        finally:
            db.close()
