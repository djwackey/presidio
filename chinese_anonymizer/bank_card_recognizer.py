from presidio_analyzer import Pattern, PatternRecognizer


class ChineseBankCardRecognizer(PatternRecognizer):
    def __init__(self):
        bank_card_patterns = [
            Pattern(
                name="bank_card",
                regex=r"\b(62\d{14,17}|94\d{14,17}|35\d{14,17}|5[1-5]\d{14}|4\d{15})\b",
                score=0.85,
            ),
            Pattern(
                name="bank_card_with_spaces",
                regex=r"\b(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4,7})\b",
                score=0.75,
            )
        ]
        super().__init__(
            supported_entity="BANK_CARD",
            patterns=bank_card_patterns,
            supported_language="zh"
        )