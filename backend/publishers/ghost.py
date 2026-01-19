"""
Ghost API集成
"""
import requests
import logging

logger = logging.getLogger(__name__)

class GhostPublisher:
    """Ghost内容发布器"""
    
    def __init__(self, ghost_url, admin_api_key):
        self.ghost_url = ghost_url.rstrip('/')
        self.admin_api_key = admin_api_key
        self.api_url = f"{self.ghost_url}/ghost/api/admin"
        self.headers = {
            'Authorization': f'Ghost {self.admin_api_key}',
            'Content-Type': 'application/json'
        }
    
    def publish_post(self, title, content, status='published'):
        """
        发布文章到Ghost
        status: 'draft' 或 'published'
        """
        try:
            url = f"{self.api_url}/posts/"
            
            payload = {
                "posts": [{
                    "title": title,
                    "html": content,  # Ghost支持HTML
                    "status": status,
                    "tags": ["情报推送", "实时快讯"]
                }]
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            post_id = result['posts'][0]['id']
            
            logger.info(f"Successfully published to Ghost: {post_id}")
            
            return {
                'success': True,
                'post_id': post_id,
                'url': f"{self.ghost_url}/{result['posts'][0]['slug']}/"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error publishing to Ghost: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self):
        """测试连接"""
        try:
            url = f"{self.api_url}/site/"
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            return True
        except:
            return False
