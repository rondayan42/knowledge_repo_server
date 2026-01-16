"""
Articles model for Knowledge Repository - SQLAlchemy version
"""

import re
from datetime import datetime
from sqlalchemy import func, or_
from database import get_db
from models.orm import Article, Category, Department, Priority, Tag, ArticleTag, Attachment


class Articles:
    @staticmethod
    def get_all(filters=None):
        if filters is None:
            filters = {}
        
        db = get_db()
        try:
            query = db.query(Article)
            
            if filters.get('category_id'):
                query = query.filter(Article.category_id == filters['category_id'])
            
            if filters.get('department_id'):
                query = query.filter(Article.department_id == filters['department_id'])
            
            if filters.get('priority_id'):
                query = query.filter(Article.priority_id == filters['priority_id'])
            
            articles = query.order_by(Article.updated_at.desc()).all()
            return [a.to_dict() for a in articles]
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(id):
        db = get_db()
        try:
            article = db.query(Article).filter_by(id=id).first()
            return article.to_dict() if article else None
        finally:
            db.close()
    
    @staticmethod
    def create(data):
        db = get_db()
        try:
            article = Article(
                title=data.get('title'),
                summary=data.get('summary'),
                content=data.get('content'),
                category_id=data.get('category_id'),
                department_id=data.get('department_id'),
                priority_id=data.get('priority_id'),
                author=data.get('author'),
                author_id=data.get('author_id')
            )
            db.add(article)
            db.commit()
            db.refresh(article)
            
            article_id = article.id
            
            # Add tags
            tags = data.get('tags', [])
            if tags:
                Articles._set_tags_internal(db, article_id, tags, data.get('author_id'))
            
            # Link attachments
            attachment_ids = data.get('attachmentIds', [])
            if attachment_ids:
                Articles._assign_attachments_internal(db, article_id, attachment_ids)
            
            db.commit()
            
            # Return fresh article with relations
            article = db.query(Article).filter_by(id=article_id).first()
            return article.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def update(id, data):
        db = get_db()
        try:
            article = db.query(Article).filter_by(id=id).first()
            if not article:
                return None
            
            article.title = data.get('title')
            article.summary = data.get('summary')
            article.content = data.get('content')
            article.category_id = data.get('category_id')
            article.department_id = data.get('department_id')
            article.priority_id = data.get('priority_id')
            article.author = data.get('author')
            article.author_id = data.get('author_id')
            article.updated_at = datetime.utcnow()
            
            # Update tags
            tags = data.get('tags', [])
            if tags is not None:
                Articles._set_tags_internal(db, id, tags, data.get('author_id'))
            
            # Update attachments
            attachment_ids = data.get('attachmentIds', [])
            if attachment_ids is not None:
                Articles._assign_attachments_internal(db, id, attachment_ids)
            
            db.commit()
            db.refresh(article)
            return article.to_dict()
        finally:
            db.close()
    
    @staticmethod
    def delete(id):
        db = get_db()
        try:
            article = db.query(Article).filter_by(id=id).first()
            if article:
                db.delete(article)
                db.commit()
            return True
        finally:
            db.close()
    
    @staticmethod
    def _set_tags_internal(db, article_id, tag_names, author_id=None):
        """Set tags for an article (internal, uses existing db session)."""
        # Remove existing tags
        db.query(ArticleTag).filter_by(article_id=article_id).delete()
        
        # Add new tags
        for tag_name in tag_names:
            # Get or create tag
            tag = db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, created_by=author_id)
                db.add(tag)
                db.flush()  # Get tag ID
            
            # Create article-tag association
            article_tag = ArticleTag(article_id=article_id, tag_id=tag.id)
            db.merge(article_tag)  # Use merge to handle duplicates
    
    @staticmethod
    def _assign_attachments_internal(db, article_id, attachment_ids):
        """Assign attachments to an article (internal, uses existing db session)."""
        # Clear current links
        db.query(Attachment).filter_by(article_id=article_id).update({'article_id': None})
        
        # Assign new attachments
        for att_id in attachment_ids:
            db.query(Attachment).filter_by(id=att_id).update({'article_id': article_id})
    
    @staticmethod
    def set_tags(article_id, tag_names, author_id=None):
        """Set tags for an article (public API)."""
        db = get_db()
        try:
            Articles._set_tags_internal(db, article_id, tag_names, author_id)
            db.commit()
        finally:
            db.close()
    
    @staticmethod
    def increment_views(id):
        db = get_db()
        try:
            article = db.query(Article).filter_by(id=id).first()
            if article:
                article.views = (article.views or 0) + 1
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def search(search_term):
        db = get_db()
        try:
            pattern = f'%{search_term}%'
            articles = db.query(Article).filter(
                or_(
                    Article.title.ilike(pattern),
                    Article.summary.ilike(pattern),
                    Article.content.ilike(pattern)
                )
            ).order_by(Article.updated_at.desc()).all()
            
            result = []
            for article in articles:
                article_dict = article.to_dict()
                article_dict['snippet'] = Articles._generate_snippet(article_dict, search_term)
                article_dict['matchField'] = Articles._get_match_field(article_dict, search_term)
                result.append(article_dict)
            
            return result
        finally:
            db.close()
    
    @staticmethod
    def _generate_snippet(article, search_term):
        """Generate a snippet showing content around the search match."""
        snippet_length = 150
        term = search_term.lower()
        
        # Check title first
        if article.get('title') and term in article['title'].lower():
            return article['title']
        
        # Then summary
        if article.get('summary') and term in article['summary'].lower():
            return Articles._extract_snippet(article['summary'], search_term, snippet_length)
        
        # Finally content (strip HTML first)
        if article.get('content'):
            text_content = re.sub(r'<[^>]*>', ' ', article['content'])
            text_content = re.sub(r'\s+', ' ', text_content)
            if term in text_content.lower():
                return Articles._extract_snippet(text_content, search_term, snippet_length)
        
        return article.get('summary', '')
    
    @staticmethod
    def _extract_snippet(text, search_term, length):
        """Extract a snippet around the match."""
        lower_text = text.lower()
        lower_term = search_term.lower()
        index = lower_text.find(lower_term)
        
        if index == -1:
            return text[:length * 2]
        
        start = max(0, index - length)
        end = min(len(text), index + len(search_term) + length)
        
        snippet = text[start:end]
        if start > 0:
            snippet = '...' + snippet
        if end < len(text):
            snippet = snippet + '...'
        
        return snippet
    
    @staticmethod
    def _get_match_field(article, search_term):
        """Determine which field matched."""
        term = search_term.lower()
        if article.get('title') and term in article['title'].lower():
            return 'title'
        if article.get('summary') and term in article['summary'].lower():
            return 'summary'
        if article.get('content') and term in article['content'].lower():
            return 'content'
        return 'unknown'
    
    @staticmethod
    def get_stats():
        db = get_db()
        try:
            # Total articles count
            total_count = db.query(func.count(Article.id)).scalar()
            
            # Total views
            total_views = db.query(func.coalesce(func.sum(Article.views), 0)).scalar()
            
            # By category
            cat_stats = db.query(
                Category.name,
                func.count(Article.id).label('count')
            ).outerjoin(Article, Category.id == Article.category_id).group_by(Category.id, Category.name).all()
            
            # By department
            dep_stats = db.query(
                Department.name,
                func.count(Article.id).label('count')
            ).outerjoin(Article, Department.id == Article.department_id).group_by(Department.id, Department.name).all()
            
            # Recent articles
            recent = db.query(Article).order_by(Article.updated_at.desc()).limit(5).all()
            
            return {
                'totalArticles': total_count or 0,
                'totalViews': total_views or 0,
                'byCategory': [{'name': name, 'count': count} for name, count in cat_stats],
                'byDepartment': [{'name': name, 'count': count} for name, count in dep_stats],
                'recentArticles': [{'id': a.id, 'title': a.title, 'updated_at': a.updated_at.isoformat() if a.updated_at else None} for a in recent]
            }
        finally:
            db.close()
