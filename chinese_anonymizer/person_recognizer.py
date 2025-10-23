"""
中文人名识别器
Chinese Person Name Recognizer
"""

from typing import List, Optional
import re
from presidio_analyzer import Pattern, PatternRecognizer


class ChinesePersonRecognizer(PatternRecognizer):
    """
    识别中文人名的识别器
    Recognizer for Chinese person names
    """
    
    # 常见的中文姓氏（部分）
    COMMON_SURNAMES = [
        "张", "王", "李", "赵", "陈", "刘", "杨", "黄", "周", "吴",
        "徐", "孙", "马", "朱", "胡", "林", "郭", "何", "高", "罗",
        "郑", "梁", "谢", "宋", "唐", "许", "邓", "冯", "韩", "曹",
        "彭", "曾", "萧", "田", "董", "潘", "袁", "于", "蒋", "蔡",
        "余", "杜", "叶", "程", "魏", "苏", "吕", "丁", "任", "沈"
    ]
    
    # 构建姓氏模式
    surnames_pattern = "|".join(COMMON_SURNAMES)
    
    PATTERNS = [
        # 姓氏 + 1-2个字的名字
        Pattern("CHINESE_NAME_PATTERN", 
               rf"\b({surnames_pattern})[\u4e00-\u9fff]{{1,2}}\b", 0.8),
        # 三字姓名（可能是复姓）
        Pattern("CHINESE_THREE_CHAR_NAME", 
               r"\b[\u4e00-\u9fff]{3}\b", 0.6),
        # 两字姓名
        Pattern("CHINESE_TWO_CHAR_NAME", 
               rf"\b({surnames_pattern})[\u4e00-\u9fff]\b", 0.7),
    ]
    
    CONTEXT = [
        "姓名", "名字", "称呼", "患者", "病人", "先生", "女士", "同志",
        "name", "patient", "person", "mr", "ms", "男", "女"
    ]
    
    def __init__(self):
        super().__init__(
            supported_entity="PERSON",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="zh"
        )