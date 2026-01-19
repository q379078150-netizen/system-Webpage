"""
Telegram Bot集成
"""
import requests
import logging

logger = logging.getLogger(__name__)

class TelegramPublisher:
    """Telegram消息发布器"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, text, parse_mode='HTML'):
        """
        发送消息到Telegram
        parse_mode: 'HTML' 或 'Markdown'
        """
        try:
            url = f"{self.api_url}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            message_id = result['result']['message_id']
            
            logger.info(f"Successfully sent to Telegram: {message_id}")
            
            return {
                'success': True,
                'message_id': message_id
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending to Telegram: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self):
        """测试连接"""
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return True
        except:
            return False
