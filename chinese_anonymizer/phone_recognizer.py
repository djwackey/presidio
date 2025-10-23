"""
中文电话号码识别器
Chinese Phone Number Recognizer
"""

from typing import List, Optional
import re
from presidio_analyzer import Pattern, PatternRecognizer


class ChinesePhoneRecognizer(PatternRecognizer):
    """
    识别中国大陆手机号码的识别器
    Recognizer for Chinese mainland mobile phone numbers
    """
    
    PATTERNS = [
        Pattern("CHINESE_PHONE_PATTERN", 
               r"\b1[3-9]\d{9}\b", 0.9),
        Pattern("CHINESE_PHONE_WITH_SPACES", 
               r"\b1[3-9]\d\s?\d{4}\s?\d{4}\b", 0.8),
        Pattern("CHINESE_PHONE_WITH_DASHES", 
               r"\b1[3-9]\d-\d{4}-\d{4}\b", 0.8),
    ]
    
    CONTEXT = [
        "电话", "手机", "联系方式", "手机号", "电话号码", "联系电话",
        "phone", "mobile", "tel", "contact"
    ]
    
    def __init__(self):
        super().__init__(
            supported_entity="PHONE_NUMBER",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="zh"
        )