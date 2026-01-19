"""
配置文件 - 情报推送系统
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    os.makedirs(DATABASE_DIR, exist_ok=True)
    DATABASE_URL = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(DATABASE_DIR, "intelligence.db")}'
    
    # Ghost配置
    GHOST_URL = os.environ.get('GHOST_URL', '').rstrip('/')
    GHOST_ADMIN_API_KEY = os.environ.get('GHOST_ADMIN_API_KEY', '')
    GHOST_CONTENT_API_KEY = os.environ.get('GHOST_CONTENT_API_KEY', '')
    
    # Telegram配置
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
    
    # Discord配置
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '')
    
    # Insight.ai配置（Ghost实例）
    INSIGHT_AI_GHOST_URL = os.environ.get('INSIGHT_AI_GHOST_URL', '').rstrip('/')
    INSIGHT_AI_ADMIN_API_KEY = os.environ.get('INSIGHT_AI_ADMIN_API_KEY', '')
    
    # 推送配置
    REAL_TIME_PUSH_RATINGS = [4, 5]  # 实时推送的星级
    DIGEST_MIN_RATING = 3  # 纳入简报的最低星级
    
    # 任务调度配置
    DIGEST_GENERATION_TIME = "00:00"  # 每日简报生成时间 (UTC)
    
    # 日志配置
    LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # 管理员操作（用于删除等敏感操作）
    # 建议在 .env 中配置一个强随机值，例如：ADMIN_TOKEN=your-long-random-token
    ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', '')
