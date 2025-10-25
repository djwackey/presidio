from presidio_analyzer import Pattern, PatternRecognizer

class ChineseInpatientRecognizer(PatternRecognizer):
    def __init__(self):
        inpatient_patterns = [
            Pattern(
                name="inpatient",
                regex=r"\bZY\d{6,10}\b",
                score=0.8
            ),
            Pattern(
                name="inpatient_chinese",
                regex=r"\b住院\d{6,10}\b",
                score=0.8
            )
        ]
        super().__init__(
            supported_entity="INPATIENT_NO",
            patterns=inpatient_patterns,
            supported_language="en"
        )
