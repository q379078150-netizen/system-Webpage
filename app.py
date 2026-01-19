"""
Flask应用主入口 - 情报推送系统
"""
from flask import Flask
from config import Config
from backend.routes import register_routes
from backend.scheduler import init_scheduler
from backend.database import init_db
import os
import logging

def setup_logging():
    """配置日志系统"""
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def create_app():
    """创建Flask应用"""
    app = Flask(__name__, 
                template_folder='frontend/templates',
                static_folder='frontend/static')
    app.config.from_object(Config)
    
    # 设置日志
    setup_logging()
    
    # 初始化数据库
    init_db(app)
    
    # 注册路由
    register_routes(app)
    
    # 初始化任务调度器
    init_scheduler(app)
    
    # 创建必要的目录
    os.makedirs('database', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
