from presidio_analyzer import Pattern, PatternRecognizer


class ChineseSettlementRecognizer(PatternRecognizer):
    def __init__(self):
        settlement_patterns = [
            Pattern(
                name="settlement_receipt",
                regex=r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b",
                score=0.85,
            ),
            Pattern(
                name="settlement_receipt_chinese",
                regex=r"\b结算单号[:：]\s*[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b",
                score=0.90,
            )
        ]
        super().__init__(
            supported_entity="SETTLEMENT_NO",
            patterns=settlement_patterns,
            supported_language="zh"
        )