from presidio_analyzer import Pattern, PatternRecognizer


class ChineseAddressRecognizer(PatternRecognizer):
    def __init__(self):
        address_patterns = [
            Pattern(
                name="chinese_address",
                regex=r"([\u4e00-\u9fff]{1,5}(?:省|自治区|市|县|区|镇|乡|村|街道|路|巷|弄))([\u4e00-\u9fff0-9a-zA-Z\-]+)",
                score=0.85,
            )
        ]
        super().__init__(supported_entity="ADDRESS", patterns=address_patterns, supported_language="zh")
