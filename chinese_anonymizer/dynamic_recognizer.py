from presidio_analyzer import Pattern, PatternRecognizer


class DynamicRecognizer(PatternRecognizer):
    """
    动态识别器，可以从数据库配置中加载识别模式
    Dynamic recognizer that can be configured with patterns and settings from database
    """

    def __init__(
        self,
        name: str,
        patterns: list,
        context: list,
        supported_entity: str,
        **kwargs
    ):
        """
        初始化动态识别器
        Initialize the DynamicRecognizer with configuration from database

        Args:
            name: 识别器名称
            patterns: 模式列表（Pattern对象）
            context: 上下文关键词列表
            supported_entities: 支持的实体类型列表
            **kwargs: 传递给PatternRecognizer的额外参数
        """
        super().__init__(
            name=name,
            patterns=patterns,
            context=context,
            supported_entity=supported_entity,
            **kwargs
        )
