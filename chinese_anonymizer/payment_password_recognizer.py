from presidio_analyzer import Pattern, PatternRecognizer

class ChinesePaymentPasswordRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="payment_password",
                regex=r"\b\d{6}\b",
                score=0.85,
            )
        ]
        super().__init__(
            supported_entity="PAYMENT_PASSWORD",
            patterns=patterns,
            supported_language="zh"
        )