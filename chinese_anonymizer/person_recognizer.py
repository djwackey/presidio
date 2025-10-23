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
        # 姓氏 + 1-2个字的名字，前后有分隔符或特定上下文
        Pattern("CHINESE_NAME_WITH_CONTEXT", 
               rf"(?<=患者|病人|姓名|名字)[\s：:]*({surnames_pattern})[\u4e00-\u9fff]{{1,2}}", 0.95),
        # 姓氏 + 1-2个字的名字，在句首或标点后
        Pattern("CHINESE_NAME_PATTERN", 
               rf"(?<=^|[，。！？\s])({surnames_pattern})[\u4e00-\u9fff]{{1,2}}(?=[，。！？\s]|$)", 0.9),
        # 姓氏 + 名字 + 女士/先生/同志等称谓
        Pattern("CHINESE_NAME_WITH_TITLE", 
               rf"({surnames_pattern})[\u4e00-\u9fff]{{1,2}}(?=女士|先生|同志|医生|教授|老师)", 0.95),
        # 两字姓名，增加上下文限制
        Pattern("CHINESE_TWO_CHAR_NAME", 
               rf"(?<=^|[，。！？\s])({surnames_pattern})[\u4e00-\u9fff](?=[，。！？\s]|$)", 0.8),
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
            supported_language="en"  # 使用 "en" 以便与默认配置兼容
        )