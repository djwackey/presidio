"""
中文文本脱敏引擎
Chinese Text Anonymization Engine
"""

from typing import Dict, List, Optional

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from .address_recognizer import ChineseAddressRecognizer
from .bank_card_recognizer import ChineseBankCardRecognizer
from .datetime_recognizer import ChineseDateTimeRecognizer
from .id_card_recognizer import ChineseIdCardRecognizer
from .inpatient_recognizer import ChineseInpatientRecognizer
from .outpatient_recognizer import ChineseOutpatientRecognizer
from .payment_amount_recognizer import ChinesePaymentAmountRecognizer
from .payment_password_recognizer import ChinesePaymentPasswordRecognizer
from .person_recognizer import ChinesePersonRecognizer
from .phone_recognizer import ChinesePhoneRecognizer
from .settlement_recognizer import ChineseSettlementRecognizer
from .medical_test_recognizer import ChineseMedicalTestRecognizer


class ChineseAnonymizer:
    """
    中文文本脱敏引擎
    Chinese Text Anonymization Engine
    """

    def __init__(self, profile_name="default"):
        """初始化中文脱敏引擎"""
        self.profile_name = profile_name
        self.analyzer = None
        self.anonymizer = AnonymizerEngine()

    async def init(self):
        self.analyzer = await self._setup_analyzer()

    async def _setup_analyzer(self) -> AnalyzerEngine:
        """设置分析器，包含中文语言支持和自定义识别器"""
        # 创建识别器注册表
        registry = RecognizerRegistry()
        registry.supported_languages = ["zh"]

        # 从数据库加载识别器配置
        try:
            from .db_connector import DatabaseConnector
            import importlib

            db = DatabaseConnector()
            profile = await db.get_profile_settings(profile_name=self.profile_name)
            await db.close()
            if not profile:
                raise ValueError("Profile not found.Fallback to hardcoded recognizers")

            self.anonymize_entities = profile.get("anonymize_entities", {})

            from presidio_analyzer import Pattern

            for recognizer in profile["recognizers"]:
                try:
                    class_name = recognizer["class_name"]
                    module_path = recognizer["module_path"]
                    # print(f"[class_name] {class_name}")
                    # print(f"[module_path] {module_path}")
                    module = importlib.import_module(module_path)
                    recognizer_cls = getattr(module, class_name)
                    # print(f"[recognizer] {recognizer}")
                    # print(f"[anonymize_entities] {self.anonymize_entities}")

                    # Handle dynamic recognizer configuration
                    if class_name == "DynamicRecognizer":
                        # Convert pattern dicts to Pattern objects
                        pattern_objects = [
                            Pattern(name=p["name"], regex=p["regex"], score=p["score"])
                            for p in recognizer.get("patterns", [])
                        ]

                        # Create DynamicRecognizer instance with parameters
                        instance = recognizer_cls(
                            name=f"Dynamic_{recognizer['id']}",
                            patterns=pattern_objects,
                            context=recognizer.get("context", []),
                            supported_entity=recognizer.get("supported_entity", ""),
                            supported_language="zh",
                            # score_threshold=recognizer.get("score_threshold", 0.5)
                        )
                        registry.add_recognizer(instance)
                    else:
                        # Regular recognizer instantiation
                        registry.add_recognizer(recognizer_cls())
                except (ImportError, AttributeError) as e:
                    print(f"Error loading recognizer {recognizer['id']}: {e}")
        except Exception as e:
            print(f"Database error: {e}. Using default recognizers.")
            self._add_default_recognizers(registry)

        # 获取默认识别器并添加到注册表
        # registry.load_predefined_recognizers()

        # 创建支持中文的分析器
        nlp_configuration = {
            # spaCy官方提供的最小中文模型
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "zh", "model_name": "zh_core_web_sm"}],
            # "nlp_engine_name": "spacy",
            # "models": [{"lang_code": "zh", "model_name": "zh_core_web_lg"}],
        }
        provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
        nlp_engine = provider.create_engine()
        analyzer = AnalyzerEngine(
            default_score_threshold=0.5, nlp_engine=nlp_engine, registry=registry, supported_languages=["zh"]
        )

        return analyzer

    def _add_default_recognizers(self, registry):
        """Add default hardcoded recognizers as fallback"""
        registry.add_recognizer(ChineseIdCardRecognizer())
        registry.add_recognizer(ChinesePhoneRecognizer())
        registry.add_recognizer(ChinesePersonRecognizer())
        registry.add_recognizer(ChineseInpatientRecognizer())
        registry.add_recognizer(ChineseOutpatientRecognizer())
        registry.add_recognizer(ChineseAddressRecognizer())
        registry.add_recognizer(ChineseBankCardRecognizer())
        registry.add_recognizer(ChineseSettlementRecognizer())
        registry.add_recognizer(ChinesePaymentPasswordRecognizer())
        registry.add_recognizer(ChinesePaymentAmountRecognizer())
        registry.add_recognizer(ChineseDateTimeRecognizer())
        registry.add_recognizer(ChineseMedicalTestRecognizer())

    def analyze(self, text: str, entities: Optional[List[str]] = None, language: str = "zh"):
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
        language: str = "zh",
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
        print("检测到的实体:")
        for result in analyzer_results:
            print(
                f"  - 类型: {result.entity_type}, 文本: '{text[result.start:result.end]}', 位置: {result.start}-{result.end}, 置信度: {result.score:.2f}"
            )
        print()
        return self.anonymize(text=text, analyzer_results=analyzer_results, anonymize_entities=anonymize_entities)
