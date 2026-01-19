"""
每日简报生成器
"""
from flask import Flask
from backend.database import db
from backend.models import Intelligence, DailyDigest
from backend.publishers.ghost import GhostPublisher
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class DailyDigestGenerator:
    """每日简报生成器"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.config = app.config
        
        # Insight.ai Ghost发布器
        self.ghost_publisher = None
        if self.config.get('INSIGHT_AI_GHOST_URL') and self.config.get('INSIGHT_AI_ADMIN_API_KEY'):
            self.ghost_publisher = GhostPublisher(
                self.config['INSIGHT_AI_GHOST_URL'],
                self.config['INSIGHT_AI_ADMIN_API_KEY']
            )
    
    def generate(self, target_date=None):
        """
        生成指定日期的简报
        汇总所有3星以上情报
        """
        if target_date is None:
            target_date = date.today().isoformat()
        
        try:
            # 查询当日所有3星以上情报
            min_rating = self.config.get('DIGEST_MIN_RATING', 3)
            
            with self.app.app_context():
                # 解析日期
                if isinstance(target_date, str):
                    target_date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
                else:
                    target_date_obj = target_date
                
                # 查询当日情报
                from sqlalchemy import func
                intelligence_list = Intelligence.query.filter(
                    Intelligence.rating >= min_rating,
                    func.date(Intelligence.created_at) == target_date_obj
                ).order_by(Intelligence.rating.desc(), Intelligence.created_at.desc()).all()
                
                if not intelligence_list:
                    logger.warning(f"No intelligence found for {target_date}")
                    return None
                
                # 生成简报内容
                content = self._generate_content(intelligence_list, target_date_obj)
                
                # 保存或更新简报
                digest = DailyDigest.query.filter_by(date=target_date).first()
                
                if digest:
                    digest.content = content
                    digest.status = 'draft'
                else:
                    digest = DailyDigest(
                        date=target_date,
                        content=content,
                        status='draft'
                    )
                    db.session.add(digest)
                
                db.session.commit()
                
                logger.info(f"Generated digest for {target_date} with {len(intelligence_list)} items")
                
                return digest
                
        except Exception as e:
            logger.error(f"Error generating digest: {str(e)}")
            raise
    
    def _generate_content(self, intelligence_list, target_date):
        """生成简报HTML内容"""
        html = f"""
        <h1>每日情报简报 - {target_date}</h1>
        <p>本日共收录 <strong>{len(intelligence_list)}</strong> 条重要情报</p>
        <hr>
        """
        
        # 按星级分组
        by_rating = {}
        for item in intelligence_list:
            rating = item.rating
            if rating not in by_rating:
                by_rating[rating] = []
            by_rating[rating].append(item)
        
        # 按星级从高到低排列
        for rating in sorted(by_rating.keys(), reverse=True):
            stars = "⭐" * rating
            html += f"<h2>{stars} {rating}星情报</h2>\n"
            
            for item in by_rating[rating]:
                html += f"""
                <div style="margin-bottom: 20px; padding: 15px; border-left: 4px solid #3498db; background-color: #f8f9fa;">
                    <h3>{item.title}</h3>
                    <p>{item.content}</p>
                    <small>来源: {item.source or '未知'} | 时间: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}</small>
                </div>
                """
        
        html += "<hr><p><em>本简报由情报推送系统自动生成</em></p>"
        
        return html
    
    def publish(self, digest: DailyDigest):
        """发布简报到Ghost"""
        if not self.ghost_publisher:
            raise Exception("Ghost publisher not configured for Insight.ai")
        
        try:
            title = f"每日情报简报 - {digest.date}"
            
            result = self.ghost_publisher.publish_post(
                title,
                digest.content,
                status='published'
            )
            
            if result.get('success'):
                with self.app.app_context():
                    digest.ghost_post_id = result.get('post_id')
                    digest.status = 'published'
                    digest.published_at = datetime.utcnow()
                    db.session.commit()
                
                logger.info(f"Published digest {digest.id} to Insight.ai")
            
            return result
            
        except Exception as e:
            logger.error(f"Error publishing digest: {str(e)}")
            raise
