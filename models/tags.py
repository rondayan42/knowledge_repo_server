"""
Tags model for Knowledge Repository - SQLAlchemy version
"""

from database import get_db
from models.orm import Tag, ArticleTag


class Tags:
    @staticmethod
    def get_all():
        db = get_db()
        try:
            tags = db.query(Tag).order_by(Tag.name).all()
            return [t.to_dict() for t in tags]
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            tag = db.query(Tag).filter_by(id=id).first()
            return tag.to_dict() if tag else None
        finally:
            db.close()
    
    @staticmethod
    def get_by_name(name):
        db = get_db()
        try:
            tag = db.query(Tag).filter_by(name=name).first()
            return tag.to_dict() if tag else None
        finally:
            db.close()
    
    @staticmethod
    def create(name, creator_id=None):
        db = get_db()
        try:
            # Check if tag already exists
            existing = db.query(Tag).filter_by(name=name).first()
            if existing:
                return existing.to_dict()
            
            tag = Tag(name=name, created_by=creator_id)
            db.add(tag)
            db.commit()
            db.refresh(tag)
            return tag.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def delete(id):
        db = get_db()
        try:
            tag = db.query(Tag).filter_by(id=id).first()
            if tag:
                db.delete(tag)
                db.commit()
            return True
        finally:
            db.close()
    
    @staticmethod
    def get_by_article_id(article_id):
        db = get_db()
        try:
            article_tags = db.query(ArticleTag).filter_by(article_id=article_id).all()
            tags = []
            for at in article_tags:
                tag = db.query(Tag).filter_by(id=at.tag_id).first()
                if tag:
                    tags.append(tag.to_dict())
            return sorted(tags, key=lambda t: t['name'])
        finally:
            db.close()
