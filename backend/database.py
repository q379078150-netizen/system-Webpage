"""
数据库初始化和管理
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app: Flask):
    """初始化数据库"""
    # 设置数据库URI
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE_URL', 'sqlite:///database/intelligence.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        app.logger.info("Database initialized successfully")
