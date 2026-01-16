"""
Attachments model for Knowledge Repository - SQLAlchemy version
"""

from database import get_db
from models.orm import Attachment


class Attachments:
    @staticmethod
    def create(article_id=None, file_name=None, mime_type=None, size=None, url=None):
        db = get_db()
        try:
            attachment = Attachment(
                article_id=article_id,
                file_name=file_name,
                mime_type=mime_type,
                size=size,
                url=url
            )
            db.add(attachment)
            db.commit()
            db.refresh(attachment)
            return attachment.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            attachment = db.query(Attachment).filter_by(id=id).first()
            return attachment.to_dict() if attachment else None
        finally:
            db.close()
    
    @staticmethod
    def get_by_article_id(article_id):
        db = get_db()
        try:
            attachments = db.query(Attachment).filter_by(article_id=article_id).order_by(Attachment.created_at.desc()).all()
            return [a.to_dict() for a in attachments]
        finally:
            db.close()
    
    @staticmethod
    def detach_from_article(article_id):
        db = get_db()
        try:
            db.query(Attachment).filter_by(article_id=article_id).update({'article_id': None})
            db.commit()
        finally:
            db.close()
    
    @staticmethod
    def assign_to_article(article_id, attachment_ids):
        if not attachment_ids:
            return
        
        db = get_db()
        try:
            # Clear current links
            db.query(Attachment).filter_by(article_id=article_id).update({'article_id': None})
            
            # Assign new attachments
            for att_id in attachment_ids:
                db.query(Attachment).filter_by(id=att_id).update({'article_id': article_id})
            
            db.commit()
        finally:
            db.close()
