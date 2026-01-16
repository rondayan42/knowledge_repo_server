"""
Recently Viewed model for Knowledge Repository - SQLAlchemy version
"""

from datetime import datetime, timedelta
from sqlalchemy import text
from database import get_db
from models.orm import RecentlyViewed as RecentlyViewedModel, Article, Category, Department


class RecentlyViewed:
    @staticmethod
    def get_user_recently_viewed(user_id, limit=20):
        db = get_db()
        try:
            three_days_ago = datetime.utcnow() - timedelta(days=3)
            
            views = db.query(RecentlyViewedModel).filter(
                RecentlyViewedModel.user_id == user_id,
                RecentlyViewedModel.viewed_at > three_days_ago
            ).order_by(RecentlyViewedModel.viewed_at.desc()).limit(limit).all()
            
            result = []
            for view in views:
                article = db.query(Article).filter_by(id=view.article_id).first()
                if article:
                    category = db.query(Category).filter_by(id=article.category_id).first() if article.category_id else None
                    department = db.query(Department).filter_by(id=article.department_id).first() if article.department_id else None
                    result.append({
                        'article_id': view.article_id,
                        'viewed_at': view.viewed_at.isoformat() if view.viewed_at else None,
                        'title': article.title,
                        'summary': article.summary,
                        'category': category.name if category else None,
                        'department': department.name if department else None
                    })
            return result
        finally:
            db.close()
    
    @staticmethod
    def add_view(user_id, article_id):
        db = get_db()
        try:
            # Update existing or insert new
            existing = db.query(RecentlyViewedModel).filter_by(user_id=user_id, article_id=article_id).first()
            if existing:
                existing.viewed_at = datetime.utcnow()
            else:
                view = RecentlyViewedModel(user_id=user_id, article_id=article_id, viewed_at=datetime.utcnow())
                db.add(view)
            db.commit()
            
            # Keep only last 20 for this user
            user_views = db.query(RecentlyViewedModel).filter_by(user_id=user_id).order_by(RecentlyViewedModel.viewed_at.desc()).all()
            if len(user_views) > 20:
                for old_view in user_views[20:]:
                    db.delete(old_view)
                db.commit()
            
            # Delete entries older than 3 days
            three_days_ago = datetime.utcnow() - timedelta(days=3)
            db.query(RecentlyViewedModel).filter(
                RecentlyViewedModel.user_id == user_id,
                RecentlyViewedModel.viewed_at < three_days_ago
            ).delete()
            db.commit()
            
            return {'success': True}
        finally:
            db.close()
    
    @staticmethod
    def clear_user_history(user_id):
        db = get_db()
        try:
            db.query(RecentlyViewedModel).filter_by(user_id=user_id).delete()
            db.commit()
            return {'success': True}
        finally:
            db.close()
    
    @staticmethod
    def cleanup_old_entries():
        db = get_db()
        try:
            three_days_ago = datetime.utcnow() - timedelta(days=3)
            result = db.query(RecentlyViewedModel).filter(RecentlyViewedModel.viewed_at < three_days_ago).delete()
            db.commit()
            return {'deleted': result}
        finally:
            db.close()
