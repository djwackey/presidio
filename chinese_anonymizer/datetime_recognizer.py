from presidio_analyzer import Pattern, PatternRecognizer


class ChineseDateTimeRecognizer(PatternRecognizer):
    def __init__(self):
        datetime_patterns = [
            Pattern(
                name="chinese_date",
                regex=r"\b\d{4}年\d{1,2}月\d{1,2}日\b|\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",
                score=0.85,
            ),
            Pattern(
                name="chinese_time",
                regex=r"\b\d{1,2}[:：]\d{1,2}(?::\d{1,2})?\b|\b\d{1,2}点\d{1,2}分(?:\d{1,2}秒)?\b",
                score=0.80,
            ),
            Pattern(
                name="chinese_datetime",
                regex=r"\b\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}[:：]\d{1,2}\b|\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}[:：]\d{1,2}\b",
                score=0.90,
            )
        ]
        super().__init__(
            supported_entity="DATE_TIME",
            patterns=datetime_patterns,
            supported_language="zh"
        )
