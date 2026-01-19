"""
数据模型
"""
from backend.database import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class Intelligence(db.Model):
    """情报模型"""
    __tablename__ = 'intelligence'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(200))
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    status = Column(String(50), default='pending')  # pending, published, archived
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    
    # 关系
    push_logs = relationship('PushLog', back_populates='intelligence', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'rating': self.rating,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }

class PushLog(db.Model):
    """推送日志模型"""
    __tablename__ = 'push_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    intelligence_id = Column(Integer, ForeignKey('intelligence.id'), nullable=False)
    channel = Column(String(50), nullable=False)  # ghost, telegram, discord
    status = Column(String(50), nullable=False)  # success, failed, pending
    message = Column(Text)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    intelligence = relationship('Intelligence', back_populates='push_logs')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'intelligence_id': self.intelligence_id,
            'channel': self.channel,
            'status': self.status,
            'message': self.message,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DailyDigest(db.Model):
    """每日简报模型"""
    __tablename__ = 'daily_digest'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), unique=True, nullable=False)  # YYYY-MM-DD
    content = Column(Text, nullable=False)
    ghost_post_id = Column(String(200))
    status = Column(String(50), default='draft')  # draft, published
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'date': self.date,
            'content': self.content,
            'ghost_post_id': self.ghost_post_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
