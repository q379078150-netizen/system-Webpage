"""
任务调度器 - 定时任务管理
"""
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from backend.digest.generator import DailyDigestGenerator
from datetime import date
import logging

logger = logging.getLogger(__name__)

scheduler = None

def init_scheduler(app: Flask):
    """初始化任务调度器"""
    global scheduler
    
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.start()
        logger.info("Scheduler started")
    
    # 注册每日简报生成任务
    register_digest_job(app)
    
    return scheduler

def register_digest_job(app: Flask):
    """注册每日简报生成任务"""
    def generate_daily_digest():
        """生成每日简报"""
        try:
            with app.app_context():
                generator = DailyDigestGenerator(app)
                digest = generator.generate()
                
                if digest:
                    # 自动发布
                    try:
                        generator.publish(digest)
                        logger.info(f"Auto-generated and published digest for {date.today()}")
                    except Exception as e:
                        logger.error(f"Error auto-publishing digest: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating daily digest: {str(e)}")
    
    # 从配置读取生成时间
    config = app.config
    time_str = config.get('DIGEST_GENERATION_TIME', '00:00')
    hour, minute = map(int, time_str.split(':'))
    
    # 每天指定时间执行
    scheduler.add_job(
        func=generate_daily_digest,
        trigger=CronTrigger(hour=hour, minute=minute),
        id='daily_digest',
        name='Generate Daily Digest',
        replace_existing=True
    )
    
    logger.info(f"Scheduled daily digest generation at {time_str} UTC")
