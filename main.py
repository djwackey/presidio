#!/usr/bin/env python3
"""
中文文本脱敏演示脚本
Chinese Text Anonymization Demo Script

这个脚本演示如何使用 Presidio 对中文文本进行脱敏处理
This script demonstrates how to use Presidio for Chinese text anonymization
"""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from chinese_anonymizer.phone_recognizer import ChinesePhoneRecognizer
from chinese_anonymizer.person_recognizer import ChinesePersonRecognizer
from presidio_analyzer import RecognizerRegistry


def setup_chinese_analyzer():
    """设置支持中文的分析器"""
    # 创建识别器注册表
    registry = RecognizerRegistry()
    
    # 添加中文识别器
    registry.add_recognizer(ChinesePhoneRecognizer())
    registry.add_recognizer(ChinesePersonRecognizer())
    
    # 加载预定义识别器
    registry.load_predefined_recognizers()
    
    # 创建分析器
    analyzer = AnalyzerEngine(
        registry=registry,
        supported_languages=["zh", "en"]
    )
    
    return analyzer


def main():
    """主函数 - 演示脱敏功能"""
    
    # 测试文本
    text = "张三，男，45岁。电话：13800138000。诊断结果：高血压。"
    
    print("原始文本:", text)
    print()
    
    # 创建分析器和脱敏器
    analyzer = setup_chinese_analyzer()
    anonymizer = AnonymizerEngine()
    
    # 分析文本中的敏感实体
    results = analyzer.analyze(text=text, language='zh', entities=["PHONE_NUMBER", "PERSON"])
    
    print("检测到的实体:")
    for result in results:
        print(f"  - 类型: {result.entity_type}, 文本: '{text[result.start:result.end]}', 位置: {result.start}-{result.end}, 置信度: {result.score:.2f}")
    print()
    
    # 脱敏处理
    anonymized_text = anonymizer.anonymize(
        text=text, 
        analyzer_results=results,
        operators={"PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"}, 
                  "PERSON": {"type": "replace", "new_value": "<NAME>"}}
    )
    
    print("脱敏结果:", anonymized_text.text)
    
    # 演示其他测试用例
    print("\n" + "="*50)
    print("其他测试用例:")
    
    test_cases = [
        "患者李明，联系电话：15912345678",
        "王小红女士的手机号是13612345678",
        "赵刚先生，电话 138-1234-5678"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"原文: {test_text}")
        
        results = analyzer.analyze(text=test_text, language='zh', entities=["PHONE_NUMBER", "PERSON"])
        anonymized = anonymizer.anonymize(
            text=test_text,
            analyzer_results=results,
            operators={"PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"}, 
                      "PERSON": {"type": "replace", "new_value": "<NAME>"}}
        )
        
        print(f"脱敏: {anonymized.text}")


if __name__ == "__main__":
    main()