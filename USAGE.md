# 使用说明 / Usage Instructions

## 中文版

### 快速启动

1. **安装依赖**：
   ```bash
   # 如果还没有激活虚拟环境
   source venv/bin/activate
   
   # 如果没有安装依赖，运行
   pip install -r requirements.txt
   python -m spacy download zh_core_web_sm
   ```

2. **运行演示**：
   ```bash
   python demo_simple.py     # 运行简单演示
   python main.py           # 运行完整演示（含多个测试用例）
   ```

### 核心功能

本项目实现了基于 Microsoft Presidio 的中文文本脱敏工具，支持：

- **中文人名识别**：基于常见姓氏模式和上下文
- **中文手机号识别**：支持 13x-19x 开头的 11 位手机号
- **灵活的脱敏规则**：可自定义替换文本

### 使用示例

```python
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from chinese_anonymizer.phone_recognizer import ChinesePhoneRecognizer
from chinese_anonymizer.person_recognizer import ChinesePersonRecognizer

# 设置分析器
registry = RecognizerRegistry()
registry.add_recognizer(ChinesePhoneRecognizer())
registry.add_recognizer(ChinesePersonRecognizer())

analyzer = AnalyzerEngine(registry=registry, supported_languages=["en"])

# 分析文本
text = "张三，男，45岁。电话：13800138000。诊断结果：高血压。"
results = analyzer.analyze(text=text, language='en', entities=["PHONE_NUMBER", "PERSON"])

# 脱敏处理
anonymizer = AnonymizerEngine()
operators = {
    "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
    "PERSON": OperatorConfig("replace", {"new_value": "<NAME>"})
}

anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
print(anonymized_text.text)
# 输出: <NAME>，男，45岁。电话：<PHONE>。诊断结果：高血压。
```

### 支持的实体类型

- **PERSON**：中文人名
  - 支持 2-3 字姓名
  - 基于常见姓氏（张、王、李、赵等）
  - 支持上下文匹配（患者xxx、xxx先生/女士等）

- **PHONE_NUMBER**：中文手机号
  - 11位数字格式：13812345678
  - 带分隔符格式：138-1234-5678
  - 带空格格式：138 1234 5678

---

## English Version

### Quick Start

1. **Install Dependencies**:
   ```bash
   # If virtual environment is not activated
   source venv/bin/activate
   
   # If dependencies are not installed
   pip install -r requirements.txt
   python -m spacy download zh_core_web_sm
   ```

2. **Run Demos**:
   ```bash
   python demo_simple.py     # Run simple demo
   python main.py           # Run full demo with test cases
   ```

### Features

This project implements a Chinese text anonymization tool based on Microsoft Presidio, supporting:

- **Chinese Name Recognition**: Based on common surname patterns and context
- **Chinese Phone Number Recognition**: Supports 11-digit mobile numbers starting with 13x-19x
- **Flexible Anonymization Rules**: Customizable replacement text

### Usage Example

```python
# Same as Chinese example above
```

### Supported Entity Types

- **PERSON**: Chinese person names
  - Supports 2-3 character names
  - Based on common surnames (Zhang, Wang, Li, Zhao, etc.)
  - Context-aware matching (patient xxx, Mr./Ms. xxx, etc.)

- **PHONE_NUMBER**: Chinese mobile phone numbers
  - 11-digit format: 13812345678
  - With separators: 138-1234-5678
  - With spaces: 138 1234 5678

### Technical Notes

- Uses `supported_languages=["en"]` for compatibility with default Presidio setup
- Custom recognizers are designed to work with Chinese text while maintaining English language configuration
- Avoids conflicts with default spaCy recognizers by selective loading