from presidio_analyzer import Pattern, PatternRecognizer

class ChinesePaymentAmountRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="payment_amount_yuan",
                regex=r"\\b\\d{1,3}(?:,\\d{3})*(?:\\.\\d+)?\\s*[\\u5143]\\b",
                score=0.95,
            ),
            Pattern(
                name="payment_amount_rmb",
                regex=r"\\b\\d{1,3}(?:,\\d{3})*(?:\\.\\d+)?\\s*\\u4EBA\\u6C11\\u5E01\\b",
                score=0.95,
            ),
            Pattern(
                name="payment_amount_symbol",
                regex=r"\\b[\\xA5\\uffe5]\\d{1,3}(?:,\\d{3})*(?:\\.\\d+)?\\b",
                score=0.95,
            )
        ]
        super().__init__(
            supported_entity="PAYMENT_AMOUNT",
            patterns=patterns,
            supported_language="zh"
        )