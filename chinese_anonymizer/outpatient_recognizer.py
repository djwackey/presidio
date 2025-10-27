from presidio_analyzer import Pattern, PatternRecognizer


class ChineseOutpatientRecognizer(PatternRecognizer):
    def __init__(self):
        outpatient_patterns = [
            Pattern(name="outpatient", regex=r"\bMZ\d{6,10}\b", score=0.8),
            Pattern(name="outpatient_chinese", regex=r"\b门诊\d{6,10}\b", score=0.8),
        ]
        super().__init__(supported_entity="OUTPATIENT_NO", patterns=outpatient_patterns, supported_language="zh")
