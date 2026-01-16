"""
SQLAlchemy ORM models for Knowledge Repository
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, default='user')
    approved = Column(Boolean, default=False)
    is_root = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relationships
    favorites = relationship('UserFavorite', back_populates='user', cascade='all, delete-orphan')
    recently_viewed = relationship('RecentlyViewed', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self, include_password=False):
        data = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'approved': self.approved,
            'is_root': self.is_root,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        if include_password:
            data['password_hash'] = self.password_hash
        return data


class Category(Base):
    """Category model for organizing articles."""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    created_by = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    articles = relationship('Article', back_populates='category')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Department(Base):
    """Department model for organizing articles by department."""
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    created_by = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    articles = relationship('Article', back_populates='department')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Priority(Base):
    """Priority model for article importance levels."""
    __tablename__ = 'priorities'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    level = Column(Integer, default=0)
    color = Column(Text)
    created_by = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    articles = relationship('Article', back_populates='priority')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'color': self.color,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Tag(Base):
    """Tag model for article tagging."""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    created_by = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships (M2M through ArticleTag)
    articles = relationship('ArticleTag', back_populates='tag', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Article(Base):
    """Article model - the main content entity."""
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    summary = Column(Text)
    content = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'))
    department_id = Column(Integer, ForeignKey('departments.id', ondelete='SET NULL'))
    priority_id = Column(Integer, ForeignKey('priorities.id', ondelete='SET NULL'))
    author = Column(Text)
    author_id = Column(Text)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship('Category', back_populates='articles')
    department = relationship('Department', back_populates='articles')
    priority = relationship('Priority', back_populates='articles')
    article_tags = relationship('ArticleTag', back_populates='article', cascade='all, delete-orphan')
    attachments = relationship('Attachment', back_populates='article')
    favorites = relationship('UserFavorite', back_populates='article', cascade='all, delete-orphan')
    recently_viewed = relationship('RecentlyViewed', back_populates='article', cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        Index('idx_articles_category', 'category_id'),
        Index('idx_articles_department', 'department_id'),
        Index('idx_articles_priority', 'priority_id'),
        Index('idx_articles_created', 'created_at'),
        Index('idx_articles_title', 'title'),
    )
    
    def to_dict(self, include_relations=True):
        data = {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'category_id': self.category_id,
            'department_id': self.department_id,
            'priority_id': self.priority_id,
            'author': self.author,
            'author_id': self.author_id,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_relations:
            data['category_name'] = self.category.name if self.category else None
            data['department_name'] = self.department.name if self.department else None
            data['priority_name'] = self.priority.name if self.priority else None
            data['priority_color'] = self.priority.color if self.priority else None
            data['priority_level'] = self.priority.level if self.priority else None
            data['tags'] = [at.tag.to_dict() for at in self.article_tags]
            data['attachments'] = [a.to_dict() for a in self.attachments]
        return data


class ArticleTag(Base):
    """Junction table for Article-Tag many-to-many relationship."""
    __tablename__ = 'article_tags'
    
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    
    # Relationships
    article = relationship('Article', back_populates='article_tags')
    tag = relationship('Tag', back_populates='articles')


class Attachment(Base):
    """Attachment model for article file attachments."""
    __tablename__ = 'attachments'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='SET NULL'))
    file_name = Column(Text, nullable=False)
    mime_type = Column(Text)
    size = Column(Integer)
    url = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    article = relationship('Article', back_populates='attachments')
    
    # Indexes
    __table_args__ = (
        Index('idx_attachments_article', 'article_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'file_name': self.file_name,
            'mime_type': self.mime_type,
            'size': self.size,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserFavorite(Base):
    """User favorites - bookmarked articles."""
    __tablename__ = 'user_favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='favorites')
    article = relationship('Article', back_populates='favorites')
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_user_favorites_user', 'user_id'),
        Index('idx_user_favorites_article', 'article_id'),
    )


class RecentlyViewed(Base):
    """Recently viewed articles by users."""
    __tablename__ = 'recently_viewed'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='recently_viewed')
    article = relationship('Article', back_populates='recently_viewed')
    
    # Indexes
    __table_args__ = (
        Index('idx_recently_viewed_user', 'user_id'),
        Index('idx_recently_viewed_viewed_at', 'viewed_at'),
    )
