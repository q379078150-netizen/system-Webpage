"""
API路由定义
"""
from flask import Flask, request, jsonify
from backend.database import db
from backend.models import Intelligence, PushLog, DailyDigest
from backend.intelligence.classifier import IntelligenceClassifier
from backend.publishers.real_time_publisher import RealTimePublisher
from backend.digest.generator import DailyDigestGenerator
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def register_routes(app: Flask):
    """注册所有路由"""

    def _require_admin():
        """管理员鉴权：通过 X-Admin-Token 或 ?admin_token= 校验"""
        configured = (app.config.get('ADMIN_TOKEN') or '').strip()
        provided = (request.headers.get('X-Admin-Token') or request.args.get('admin_token') or '').strip()

        # 未配置 ADMIN_TOKEN 时，拒绝管理员操作（避免误开）
        if not configured:
            return False
        return provided == configured
    
    @app.route('/', methods=['GET'])
    def index():
        """首页 - Web界面"""
        from flask import render_template
        return render_template('index.html')
    
    @app.route('/api/docs', methods=['GET'])
    def api_docs():
        """API文档"""
        api_docs = {
            'title': '情报推送系统 API',
            'version': '1.0.0',
            'status': 'running',
            'base_url': '/api',
            'endpoints': {
                'health': {
                    'url': '/api/health',
                    'method': 'GET',
                    'description': '健康检查'
                },
                'create_intelligence': {
                    'url': '/api/intelligence',
                    'method': 'POST',
                    'description': '创建新情报',
                    'body': {
                        'title': 'string (required)',
                        'content': 'string (required)',
                        'source': 'string (optional)',
                        'rating': 'integer 1-5 (optional)'
                    }
                },
                'get_intelligence': {
                    'url': '/api/intelligence',
                    'method': 'GET',
                    'description': '获取情报列表',
                    'params': {
                        'rating': 'integer (optional)',
                        'status': 'string (optional)',
                        'limit': 'integer (optional, default: 50)'
                    }
                },
                'push_intelligence': {
                    'url': '/api/push/<intelligence_id>',
                    'method': 'POST',
                    'description': '手动触发推送'
                },
                'generate_digest': {
                    'url': '/api/digest/generate',
                    'method': 'POST',
                    'description': '生成每日简报',
                    'body': {
                        'date': 'string YYYY-MM-DD (optional)'
                    }
                }
            }
        }
        return jsonify(api_docs)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return jsonify({'status': 'ok', 'message': 'Intelligence Push System is running'})
    
    # 情报管理API
    @app.route('/api/intelligence', methods=['POST'])
    def create_intelligence():
        """创建新情报"""
        try:
            data = request.get_json()
            
            # 验证必填字段
            if not data.get('title') or not data.get('content'):
                return jsonify({'error': 'Title and content are required'}), 400
            
            # 创建情报
            intelligence = Intelligence(
                title=data['title'],
                content=data['content'],
                source=data.get('source'),
                rating=data.get('rating')
            )
            
            db.session.add(intelligence)
            db.session.commit()
            
            # 如果提供了rating，检查是否需要实时推送
            if intelligence.rating in app.config['REAL_TIME_PUSH_RATINGS']:
                publisher = RealTimePublisher(app)
                publisher.publish(intelligence)
            
            return jsonify(intelligence.to_dict()), 201
            
        except Exception as e:
            logger.error(f"Error creating intelligence: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/intelligence', methods=['GET'])
    def get_intelligence_list():
        """获取情报列表"""
        try:
            rating = request.args.get('rating', type=int)
            status = request.args.get('status')
            limit = request.args.get('limit', 50, type=int)
            
            query = Intelligence.query
            
            if rating:
                query = query.filter(Intelligence.rating == rating)
            if status:
                query = query.filter(Intelligence.status == status)
            
            intelligence_list = query.order_by(Intelligence.created_at.desc()).limit(limit).all()
            
            return jsonify([item.to_dict() for item in intelligence_list]), 200
            
        except Exception as e:
            logger.error(f"Error getting intelligence list: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/intelligence/<int:intelligence_id>', methods=['GET'])
    def get_intelligence(intelligence_id):
        """获取单个情报"""
        try:
            intelligence = Intelligence.query.get_or_404(intelligence_id)
            return jsonify(intelligence.to_dict()), 200
        except Exception as e:
            logger.error(f"Error getting intelligence: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/intelligence/<int:intelligence_id>', methods=['PUT'])
    def update_intelligence(intelligence_id):
        """更新情报"""
        try:
            intelligence = Intelligence.query.get_or_404(intelligence_id)
            data = request.get_json()
            
            if 'title' in data:
                intelligence.title = data['title']
            if 'content' in data:
                intelligence.content = data['content']
            if 'source' in data:
                intelligence.source = data['source']
            if 'rating' in data:
                intelligence.rating = data['rating']
            if 'status' in data:
                intelligence.status = data['status']
            
            intelligence.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify(intelligence.to_dict()), 200
            
        except Exception as e:
            logger.error(f"Error updating intelligence: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/intelligence/<int:intelligence_id>', methods=['DELETE'])
    def delete_intelligence(intelligence_id):
        """删除情报（仅管理员）"""
        if not _require_admin():
            return jsonify({'error': 'Admin token required'}), 403
        try:
            intelligence = Intelligence.query.get_or_404(intelligence_id)
            db.session.delete(intelligence)
            db.session.commit()
            return jsonify({'status': 'ok', 'deleted_id': intelligence_id}), 200
        except Exception as e:
            logger.error(f"Error deleting intelligence: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/intelligence/<int:intelligence_id>/classify', methods=['POST'])
    def classify_intelligence(intelligence_id):
        """手动分级情报"""
        try:
            intelligence = Intelligence.query.get_or_404(intelligence_id)
            data = request.get_json()
            rating = data.get('rating')
            
            if not rating or rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
            
            intelligence.rating = rating
            intelligence.updated_at = datetime.utcnow()
            db.session.commit()
            
            # 如果是4-5星，立即推送
            if rating in app.config['REAL_TIME_PUSH_RATINGS']:
                publisher = RealTimePublisher(app)
                publisher.publish(intelligence)
            
            return jsonify(intelligence.to_dict()), 200
            
        except Exception as e:
            logger.error(f"Error classifying intelligence: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # 推送管理API
    @app.route('/api/push/<int:intelligence_id>', methods=['POST'])
    def push_intelligence(intelligence_id):
        """手动触发推送"""
        try:
            intelligence = Intelligence.query.get_or_404(intelligence_id)
            publisher = RealTimePublisher(app)
            result = publisher.publish(intelligence)
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Error pushing intelligence: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/push/logs', methods=['GET'])
    def get_push_logs():
        """获取推送日志"""
        try:
            intelligence_id = request.args.get('intelligence_id', type=int)
            channel = request.args.get('channel')
            limit = request.args.get('limit', 100, type=int)
            
            query = PushLog.query
            
            if intelligence_id:
                query = query.filter(PushLog.intelligence_id == intelligence_id)
            if channel:
                query = query.filter(PushLog.channel == channel)
            
            logs = query.order_by(PushLog.created_at.desc()).limit(limit).all()
            
            return jsonify([log.to_dict() for log in logs]), 200
            
        except Exception as e:
            logger.error(f"Error getting push logs: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    # 简报管理API
    @app.route('/api/digest', methods=['GET'])
    def get_digest_list():
        """获取简报列表"""
        try:
            limit = request.args.get('limit', 30, type=int)
            digests = DailyDigest.query.order_by(DailyDigest.date.desc()).limit(limit).all()
            
            return jsonify([digest.to_dict() for digest in digests]), 200
            
        except Exception as e:
            logger.error(f"Error getting digest list: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/digest/generate', methods=['POST'])
    def generate_digest():
        """手动生成简报"""
        try:
            data = request.get_json()
            target_date = data.get('date', date.today().isoformat())
            
            generator = DailyDigestGenerator(app)
            digest = generator.generate(target_date)
            
            return jsonify(digest.to_dict()), 200
            
        except Exception as e:
            logger.error(f"Error generating digest: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/digest/<date_str>/publish', methods=['POST'])
    def publish_digest(date_str):
        """发布简报"""
        try:
            digest = DailyDigest.query.filter_by(date=date_str).first_or_404()
            generator = DailyDigestGenerator(app)
            result = generator.publish(digest)
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Error publishing digest: {str(e)}")
            return jsonify({'error': str(e)}), 500
