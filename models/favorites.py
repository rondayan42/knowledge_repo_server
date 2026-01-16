"""
Favorites model for Knowledge Repository - SQLAlchemy version
"""

from database import get_db
from models.orm import UserFavorite, Article, Category, Department


class Favorites:
    @staticmethod
    def get_user_favorites(user_id):
        db = get_db()
        try:
            favorites = db.query(UserFavorite).filter_by(user_id=user_id).order_by(UserFavorite.created_at.desc()).all()
            result = []
            for fav in favorites:
                article = db.query(Article).filter_by(id=fav.article_id).first()
                if article:
                    category = db.query(Category).filter_by(id=article.category_id).first() if article.category_id else None
                    department = db.query(Department).filter_by(id=article.department_id).first() if article.department_id else None
                    result.append({
                        'article_id': fav.article_id,
                        'created_at': fav.created_at.isoformat() if fav.created_at else None,
                        'title': article.title,
                        'summary': article.summary,
                        'category': category.name if category else None,
                        'department': department.name if department else None
                    })
            return result
        finally:
            db.close()
    
    @staticmethod
    def add_favorite(user_id, article_id):
        db = get_db()
        try:
            # Check if already exists
            existing = db.query(UserFavorite).filter_by(user_id=user_id, article_id=article_id).first()
            if not existing:
                favorite = UserFavorite(user_id=user_id, article_id=article_id)
                db.add(favorite)
                db.commit()
            return {'success': True}
        finally:
            db.close()
    
    @staticmethod
    def remove_favorite(user_id, article_id):
        db = get_db()
        try:
            db.query(UserFavorite).filter_by(user_id=user_id, article_id=article_id).delete()
            db.commit()
            return {'success': True}
        finally:
            db.close()
    
    @staticmethod
    def is_favorited(user_id, article_id):
        db = get_db()
        try:
            exists = db.query(UserFavorite).filter_by(user_id=user_id, article_id=article_id).first()
            return exists is not None
        finally:
            db.close()
