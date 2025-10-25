"""
中文文本脱敏引擎
Chinese Text Anonymization Engine
"""

from typing import Dict, List, Optional

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer.entities import OperatorConfig
from presidio_anonymizer import AnonymizerEngine

from .address_recognizer import ChineseAddressRecognizer
from .id_card_recognizer import ChineseIdCardRecognizer
from .inpatient_recognizer import ChineseInpatientRecognizer
from .outpatient_recognizer import ChineseOutpatientRecognizer
from .person_recognizer import ChinesePersonRecognizer
from .phone_recognizer import ChinesePhoneRecognizer


class ChineseAnonymizer:
    """
    中文文本脱敏引擎
    Chinese Text Anonymization Engine
    """

    def __init__(self):
        """初始化中文脱敏引擎"""
        self.analyzer = self._setup_analyzer()
        self.anonymizer = AnonymizerEngine()

    def _setup_analyzer(self) -> AnalyzerEngine:
        """设置分析器，包含中文语言支持和自定义识别器"""

        # 创建识别器注册表
        registry = RecognizerRegistry()

        # 添加中文识别器
        registry.add_recognizer(ChineseIdCardRecognizer())
        registry.add_recognizer(ChinesePhoneRecognizer())
        registry.add_recognizer(ChinesePersonRecognizer())
        registry.add_recognizer(ChineseInpatientRecognizer())
        registry.add_recognizer(ChineseOutpatientRecognizer())
        registry.add_recognizer(ChineseAddressRecognizer())

        # 获取默认识别器并添加到注册表
        registry.load_predefined_recognizers()

        # 创建支持中文的分析器
        analyzer = AnalyzerEngine(registry=registry, supported_languages=["en"])

        return analyzer

    def analyze(self, text: str, entities: Optional[List[str]] = None, language: str = "en"):
        """
        分析文本中的敏感实体

        Args:
            text: 待分析的文本
            entities: 要检测的实体类型列表，如 ["PHONE_NUMBER", "PERSON"]
            language: 语言代码，默认为中文 "zh"

        Returns:
            检测到的实体结果列表
        """
        return self.analyzer.analyze(text=text, language=language, entities=entities)

    def anonymize(self, text: str, analyzer_results=None, anonymize_entities: Optional[Dict[str, str]] = None):
        """
        对文本进行脱敏处理

        Args:
            text: 原始文本
            analyzer_results: 分析结果，如果为None则自动分析
            anonymize_entities: 实体类型到替换文本的映射，如 {"PHONE_NUMBER": "<PHONE>", "PERSON": "<NAME>"}

        Returns:
            脱敏后的文本结果
        """
        if analyzer_results is None:
            entities = list(anonymize_entities.keys()) if anonymize_entities else None
            analyzer_results = self.analyze(text, entities=entities)

        # 如果提供了自定义替换规则，使用替换操作符
        if anonymize_entities:
            operators = {}
            for entity_type, replacement in anonymize_entities.items():
                operators[entity_type] = OperatorConfig("replace", {"new_value": replacement})

            return self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results, operators=operators)
        else:
            # 使用默认的脱敏操作
            return self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results)

    def anonymize_text(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        anonymize_entities: Optional[Dict[str, str]] = None,
        language: str = "en",
    ):
        """
        一步完成文本分析和脱敏

        Args:
            text: 待脱敏的文本
            entities: 要检测的实体类型列表
            anonymize_entities: 实体类型到替换文本的映射
            language: 语言代码

        Returns:
            脱敏后的文本结果
        """
        analyzer_results = self.analyze(text=text, entities=entities, language=language)
        return self.anonymize(text=text, analyzer_results=analyzer_results, anonymize_entities=anonymize_entities)
