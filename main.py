#!/usr/bin/env python3
"""
中文文本脱敏演示脚本
Chinese Text Anonymization Demo Script

这个脚本演示如何使用 Presidio 对中文文本进行脱敏处理
This script demonstrates how to use Presidio for Chinese text anonymization
"""

from chinese_anonymizer.anonymizer import ChineseAnonymizer


def main():
    """主函数 - 演示脱敏功能"""
    # 创建 ChineseAnonymizer 实例
    anonymizer = ChineseAnonymizer()

    test_cases = [
        "患者李明，联系电话：15912345678",
        "王小红女士的手机号是13612345678",
        "赵刚先生，电话 138-1234-5678",
        "张三，男，45岁。电话：13800138000。诊断结果：高血压。",
        "患者王五，住院号：ZY12345678，诊断结果：糖尿病",
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"原文: {text}")

        # 执行匿名化
        anonymized_text = anonymizer.anonymize_text(text=text, anonymize_entities=anonymizer.anonymize_entities)
        print(f"脱敏: {anonymized_text.text}")


if __name__ == "__main__":
    main()
