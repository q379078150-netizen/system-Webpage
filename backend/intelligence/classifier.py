"""
情报分级系统
"""
import logging
import re

logger = logging.getLogger(__name__)

class IntelligenceClassifier:
    """情报分级器"""
    
    # 关键词权重配置
    HIGH_VALUE_KEYWORDS = {
        5: ['紧急', '重大', '突破', '暴涨', '暴跌', '危机', '重大利好', '重大利空'],
        4: ['重要', '关注', '上涨', '下跌', '趋势', '机会', '风险'],
        3: ['更新', '变化', '调整', '波动']
    }
    
    def classify(self, intelligence):
        """
        对情报进行自动分级
        返回: 1-5星评级
        """
        try:
            title = intelligence.title.lower()
            content = intelligence.content.lower()
            text = f"{title} {content}"
            
            # 计算关键词得分
            score = 0
            
            # 5星关键词
            for keyword in self.HIGH_VALUE_KEYWORDS.get(5, []):
                if keyword in text:
                    score += 10
            
            # 4星关键词
            for keyword in self.HIGH_VALUE_KEYWORDS.get(4, []):
                if keyword in text:
                    score += 5
            
            # 3星关键词
            for keyword in self.HIGH_VALUE_KEYWORDS.get(3, []):
                if keyword in text:
                    score += 2
            
            # 根据内容长度调整
            if len(content) > 500:
                score += 1
            
            # 根据来源调整（如果有）
            if intelligence.source:
                if 'official' in intelligence.source.lower():
                    score += 3
            
            # 转换为星级
            if score >= 15:
                rating = 5
            elif score >= 10:
                rating = 4
            elif score >= 5:
                rating = 3
            elif score >= 2:
                rating = 2
            else:
                rating = 1
            
            logger.info(f"Intelligence {intelligence.id} classified as {rating} stars (score: {score})")
            
            return rating
            
        except Exception as e:
            logger.error(f"Error classifying intelligence: {str(e)}")
            return 3  # 默认3星
