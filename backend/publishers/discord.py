"""
Discord Webhook集成
"""
import requests
import logging
import json

logger = logging.getLogger(__name__)

class DiscordPublisher:
    """Discord Webhook发布器"""
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def send_message(self, content, title=None, rating=None):
        """
        发送消息到Discord
        支持普通消息和嵌入消息（Embeds）
        """
        try:
            # 如果有标题和评级，使用嵌入消息
            if title or rating:
                embed = {
                    "title": title or "情报推送",
                    "description": content,
                    "color": self._get_color_by_rating(rating) if rating else 0x3498db,
                    "timestamp": None,
                    "footer": {
                        "text": f"评级: {'⭐' * rating}" if rating else "情报推送系统"
                    }
                }
                
                payload = {
                    "embeds": [embed]
                }
            else:
                payload = {
                    "content": content
                }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Successfully sent to Discord")
            
            return {
                'success': True
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending to Discord: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_color_by_rating(self, rating):
        """根据评级返回颜色（十六进制）"""
        colors = {
            5: 0xe74c3c,  # 红色
            4: 0xf39c12,  # 橙色
            3: 0x3498db,  # 蓝色
            2: 0x95a5a6,  # 灰色
            1: 0x7f8c8d   # 深灰色
        }
        return colors.get(rating, 0x3498db)
    
    def test_connection(self):
        """测试连接"""
        try:
            response = requests.get(self.webhook_url.replace('/webhooks/', '/api/webhooks/'), timeout=5)
            return response.status_code == 200
        except:
            return False
