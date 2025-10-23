# Presidio 中文文本脱敏工具

基于 Microsoft Presidio 的中文文本脱敏工具，支持检测和匿名化中文文本中的敏感信息。

## 功能特性

- 支持中文人名识别和脱敏
- 支持中文手机号码识别和脱敏  
- 基于 Microsoft Presidio 框架
- 使用 spaCy 中文语言模型
- 可自定义脱敏规则

## 快速开始

### 安装

1. 克隆项目：
```bash
git clone <repository-url>
cd presidio
```

2. 运行自动安装脚本：
```bash
./install.sh
```

或者手动安装：
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 下载中文语言模型
python -m spacy download zh_core_web_sm

# 安装项目
pip install -e .
```

### 使用示例

#### 基本用法

```python
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from chinese_anonymizer.phone_recognizer import ChinesePhoneRecognizer
from chinese_anonymizer.person_recognizer import ChinesePersonRecognizer

def setup_analyzer():
    registry = RecognizerRegistry()
    registry.add_recognizer(ChinesePhoneRecognizer())
    registry.add_recognizer(ChinesePersonRecognizer())
    registry.load_predefined_recognizers()
    return AnalyzerEngine(registry=registry, supported_languages=["zh", "en"])

text = "张三，男，45岁。电话：13800138000。诊断结果：高血压。"

analyzer = setup_analyzer()
results = analyzer.analyze(text=text, language='zh', entities=["PHONE_NUMBER", "PERSON"])
anonymizer = AnonymizerEngine()

anonymized_text = anonymizer.anonymize(
    text=text, 
    analyzer_results=results,
    operators={"PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"}, 
              "PERSON": {"type": "replace", "new_value": "<NAME>"}}
)

print("脱敏结果:", anonymized_text.text)
# 输出: 脱敏结果: <NAME>，男，45岁。电话：<PHONE>。诊断结果：高血压。
```

#### 运行演示

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行简单演示
python demo_simple.py

# 运行完整演示（包含多个测试用例）
python main.py
```

## 支持的实体类型

- **PERSON**: 中文人名（基于常见姓氏模式）
- **PHONE_NUMBER**: 中国大陆手机号码
- 其他 Presidio 默认支持的实体类型

## 项目结构

```
presidio/
├── chinese_anonymizer/          # 核心包
│   ├── __init__.py
│   ├── anonymizer.py           # 主要脱敏引擎
│   ├── person_recognizer.py    # 中文人名识别器
│   └── phone_recognizer.py     # 中文电话识别器
├── main.py                     # 完整演示脚本
├── demo_simple.py              # 简单演示脚本
├── install.sh                  # 安装脚本
├── requirements.txt            # 依赖列表
├── setup.py                    # 项目配置
└── README.md                   # 文档
```

## 技术实现

- 使用 Microsoft Presidio 作为核心框架
- 基于 spaCy 的中文语言模型 (zh_core_web_sm)
- 正则表达式匹配中国手机号码格式
- 基于常见姓氏的中文人名识别
- 支持自定义识别器扩展

## 依赖要求

- Python >= 3.8
- presidio-analyzer >= 2.2.33
- presidio-anonymizer >= 2.2.33
- spacy >= 3.4.0
- zh_core_web_sm (spaCy 中文模型)

## 许可证

MIT License
