#!/usr/bin/env python3
"""
简单演示脚本 - 使用封装好的 ChineseAnonymizer
"""
import asyncio
import json

from chinese_anonymizer.anonymizer import ChineseAnonymizer


async def main(text: str):
    # 创建 ChineseAnonymizer 实例
    anonymizer = ChineseAnonymizer(profile_name="medical_records")
    await anonymizer.init()

    # 执行匿名化
    anonymized_text = anonymizer.anonymize_text(text=text, anonymize_entities=anonymizer.anonymize_entities)
    print("脱敏: ", anonymized_text.text)


if __name__ == "__main__":
    ehr_data = []
    with open("testcases.json", "r") as f:
        ehr_data = json.loads(f.read())

    for text in ehr_data:
        asyncio.run(main(text))
