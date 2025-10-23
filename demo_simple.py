#!/usr/bin/env python3
"""
简单演示脚本 - 完全按照问题描述中的代码
Simple Demo Script - Exactly following the code from problem statement
"""

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from chinese_anonymizer.phone_recognizer import ChinesePhoneRecognizer
from chinese_anonymizer.person_recognizer import ChinesePersonRecognizer


def setup_analyzer():
    """设置分析器"""
    registry = RecognizerRegistry()
    registry.add_recognizer(ChinesePhoneRecognizer())
    registry.add_recognizer(ChinesePersonRecognizer())
    registry.load_predefined_recognizers()
    
    return AnalyzerEngine(registry=registry, supported_languages=["zh", "en"])


# 初始化全局变量以匹配问题描述中的代码结构
analyzer = setup_analyzer()
anonymizer = AnonymizerEngine()

if __name__ == "__main__":
    # 问题描述中的代码（已修正为正确的参数）
    text = "张三，男，45岁。电话：13800138000。诊断结果：高血压。"

    analyzer = setup_analyzer()  # 使用支持中文的分析器
    results = analyzer.analyze(text=text, language='zh', entities=["PHONE_NUMBER", "PERSON"])   
    anonymizer = AnonymizerEngine()
    
    # 使用正确的 operators 参数而不是 anonymize_entities
    anonymized_text = anonymizer.anonymize(
        text=text, 
        analyzer_results=results,
        operators={"PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"}, 
                  "PERSON": {"type": "replace", "new_value": "<NAME>"}}
    )
    print("脱敏: ", anonymized_text.text)