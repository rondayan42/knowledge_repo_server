"""
Departments model for Knowledge Repository - SQLAlchemy version
"""

from sqlalchemy import func
from database import get_db
from models.orm import Department, Article


class Departments:
    @staticmethod
    def get_all():
        db = get_db()
        try:
            departments = db.query(Department).order_by(Department.name).all()
            return [d.to_dict() for d in departments]
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            department = db.query(Department).filter_by(id=id).first()
            return department.to_dict() if department else None
        finally:
            db.close()
    
    @staticmethod
    def create(name, description=None, creator_id=None):
        db = get_db()
        try:
            department = Department(
                name=name,
                description=description,
                created_by=creator_id
            )
            db.add(department)
            db.commit()
            db.refresh(department)
            return department.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def update(id, name, description=None):
        db = get_db()
        try:
            department = db.query(Department).filter_by(id=id).first()
            if department:
                department.name = name
                department.description = description
                db.commit()
                db.refresh(department)
                return department.to_dict()
            return None
        finally:
            db.close()
    
    @staticmethod
    def delete(id):
        db = get_db()
        try:
            department = db.query(Department).filter_by(id=id).first()
            if department:
                db.delete(department)
                db.commit()
            return True
        finally:
            db.close()
    
    @staticmethod
    def is_in_use(id):
        db = get_db()
        try:
            count = db.query(func.count(Article.id)).filter(Article.department_id == id).scalar()
            return count > 0
        finally:
            db.close()
