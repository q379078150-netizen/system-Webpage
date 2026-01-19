"""
实时推送系统 - 4-5星情报秒级推送
"""
from flask import Flask
from backend.database import db
from backend.models import Intelligence, PushLog
from backend.publishers.ghost import GhostPublisher
from backend.publishers.telegram import TelegramPublisher
from backend.publishers.discord import DiscordPublisher
from backend.publishers.formatter import ContentFormatter
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RealTimePublisher:
    """实时推送器 - 并行推送到所有渠道"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.config = app.config
        
        # 初始化各渠道发布器
        self.ghost_publisher = None
        if self.config.get('GHOST_URL') and self.config.get('GHOST_ADMIN_API_KEY'):
            self.ghost_publisher = GhostPublisher(
                self.config['GHOST_URL'],
                self.config['GHOST_ADMIN_API_KEY']
            )
        
        self.telegram_publisher = None
        if self.config.get('TELEGRAM_BOT_TOKEN') and self.config.get('TELEGRAM_CHAT_ID'):
            self.telegram_publisher = TelegramPublisher(
                self.config['TELEGRAM_BOT_TOKEN'],
                self.config['TELEGRAM_CHAT_ID']
            )
        
        self.discord_publisher = None
        if self.config.get('DISCORD_WEBHOOK_URL'):
            self.discord_publisher = DiscordPublisher(
                self.config['DISCORD_WEBHOOK_URL']
            )
        
        self.formatter = ContentFormatter()
    
    def publish(self, intelligence: Intelligence):
        """
        推送情报到所有渠道
        返回推送结果
        """
        results = {
            'intelligence_id': intelligence.id,
            'channels': {}
        }
        
        # 格式化内容
        ghost_content = self.formatter.format_for_ghost(
            intelligence.content,
            intelligence.title,
            intelligence.rating
        )
        
        telegram_content = self.formatter.format_for_telegram(
            intelligence.content,
            intelligence.title,
            intelligence.rating
        )
        
        discord_content = self.formatter.format_for_discord(
            intelligence.content,
            intelligence.title,
            intelligence.rating
        )
        
        # 推送到Ghost
        if self.ghost_publisher:
            result = self.ghost_publisher.publish_post(
                intelligence.title,
                ghost_content,
                status='published'
            )
            self._log_push(intelligence.id, 'ghost', result)
            results['channels']['ghost'] = result
        
        # 推送到Telegram
        if self.telegram_publisher:
            result = self.telegram_publisher.send_message(telegram_content)
            self._log_push(intelligence.id, 'telegram', result)
            results['channels']['telegram'] = result
        
        # 推送到Discord
        if self.discord_publisher:
            result = self.discord_publisher.send_message(
                discord_content,
                intelligence.title,
                intelligence.rating
            )
            self._log_push(intelligence.id, 'discord', result)
            results['channels']['discord'] = result
        
        # 更新情报状态
        with self.app.app_context():
            intelligence.status = 'published'
            intelligence.published_at = datetime.utcnow()
            db.session.commit()
        
        logger.info(f"Published intelligence {intelligence.id} to all channels")
        
        return results
    
    def _log_push(self, intelligence_id, channel, result):
        """记录推送日志"""
        try:
            with self.app.app_context():
                log = PushLog(
                    intelligence_id=intelligence_id,
                    channel=channel,
                    status='success' if result.get('success') else 'failed',
                    message=str(result.get('post_id') or result.get('message_id', '')),
                    error_message=result.get('error')
                )
                db.session.add(log)
                db.session.commit()
        except Exception as e:
            logger.error(f"Error logging push: {str(e)}")
