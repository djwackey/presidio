#!/usr/bin/env python3
"""
简单演示脚本 - 使用封装好的 ChineseAnonymizer
"""
import json

from chinese_anonymizer.anonymizer import ChineseAnonymizer


def main(text: str):
    # 创建 ChineseAnonymizer 实例
    anonymizer = ChineseAnonymizer()

    # 定义要匿名化的实体和替换的标签
    anonymize_entities = {
        "PERSON": "<NAME>",
        "ADDRESS": "<ADDRESS>",
        "ID_CARD": "<ID_CARD>",
        "PHONE_NUMBER": "<PHONE>",
        "INPATIENT_NO": "<INPATIENT>",
        "OUTPATIENT_NO": "<OUTPATIENT>",
        "PAYMENT_AMOUNT": "<PAYMENT>"
    }

    # 执行匿名化
    anonymized_text = anonymizer.anonymize_text(text=text, anonymize_entities=anonymize_entities)
    print("脱敏: ", anonymized_text.text)


if __name__ == "__main__":
    ehr_data = []
    with open("testcases.json", "r") as f:
        ehr_data = json.loads(f.read())

    for text in ehr_data:
        main(text)
