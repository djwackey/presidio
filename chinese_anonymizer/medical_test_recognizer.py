from presidio_analyzer import Pattern, PatternRecognizer


class ChineseMedicalTestRecognizer(PatternRecognizer):
    def __init__(self):
        medical_test_patterns = [
            Pattern(
                name="medical_test",
                regex=r"(血常规|尿常规|心电图|X光|CT|MRI|B超|血糖|血压|体温)",
                score=0.95,
            )
        ]
        super().__init__(
            supported_entity="MEDICAL_TEST",
            patterns=medical_test_patterns,
            supported_language="zh"
        )
