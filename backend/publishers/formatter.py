"""
跨平台内容格式化
"""
import markdown
import re

class ContentFormatter:
    """内容格式化器 - 跨平台适配"""
    
    @staticmethod
    def format_for_ghost(content, title, rating=None):
        """
        格式化为Ghost格式（Markdown）
        """
        # 添加评级标签
        rating_tag = ""
        if rating:
            stars = "⭐" * rating
            rating_tag = f"**评级**: {stars}\n\n"
        
        # 转换为Markdown
        formatted = f"# {title}\n\n{rating_tag}{content}"
        
        return formatted
    
    @staticmethod
    def format_for_telegram(content, title, rating=None):
        """
        格式化为Telegram格式（HTML）
        """
        # Telegram支持HTML格式
        rating_tag = ""
        if rating:
            stars = "⭐" * rating
            rating_tag = f"<b>评级</b>: {stars}\n\n"
        
        # 转义HTML特殊字符
        title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        content_escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # 将换行符转换为HTML换行
        content_escaped = content_escaped.replace('\n', '\n')
        
        formatted = f"<b>{title_escaped}</b>\n\n{rating_tag}{content_escaped}"
        
        return formatted
    
    @staticmethod
    def format_for_discord(content, title, rating=None):
        """
        格式化为Discord格式（Markdown）
        """
        rating_tag = ""
        if rating:
            stars = "⭐" * rating
            rating_tag = f"**评级**: {stars}\n\n"
        
        # Discord使用Markdown格式
        formatted = f"**{title}**\n\n{rating_tag}{content}"
        
        return formatted
