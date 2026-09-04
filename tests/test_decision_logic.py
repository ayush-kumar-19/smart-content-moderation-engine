import unittest


MIN_CONFIDENCE = 70.0
HIGH_THRESHOLD = 90.0
MEDIUM_THRESHOLD = 70.0


def calculate_decision(labels):
    """
    Determine moderation decision and severity
    from Rekognition-style moderation labels.
    """

    if not labels:
        return "APPROVED", "LOW"

    max_confidence = max(
        float(label.get("Confidence", 0))
        for label in labels
    )

    if max_confidence >= HIGH_THRESHOLD:
        return "FLAGGED", "HIGH"

    if max_confidence >= MEDIUM_THRESHOLD:
        return "FLAGGED", "MEDIUM"

    return "APPROVED", "LOW"


class TestDecisionLogic(unittest.TestCase):

    def test_no_labels(self):
        decision, severity = calculate_decision([])

        self.assertEqual(decision, "APPROVED")
        self.assertEqual(severity, "LOW")

    def test_high_confidence(self):
        labels = [
            {
                "Name": "Weapons",
                "Confidence": 99.95
            }
        ]

        decision, severity = calculate_decision(labels)

        self.assertEqual(decision, "FLAGGED")
        self.assertEqual(severity, "HIGH")

    def test_medium_confidence(self):
        labels = [
            {
                "Name": "Violence",
                "Confidence": 80.0
            }
        ]

        decision, severity = calculate_decision(labels)

        self.assertEqual(decision, "FLAGGED")
        self.assertEqual(severity, "MEDIUM")

    def test_below_threshold(self):
        labels = [
            {
                "Name": "Example",
                "Confidence": 60.0
            }
        ]

        decision, severity = calculate_decision(labels)

        self.assertEqual(decision, "APPROVED")
        self.assertEqual(severity, "LOW")

    def test_multiple_labels_uses_highest_confidence(self):
        labels = [
            {
                "Name": "Violence",
                "Confidence": 75.0
            },
            {
                "Name": "Weapons",
                "Confidence": 95.0
            }
        ]

        decision, severity = calculate_decision(labels)

        self.assertEqual(decision, "FLAGGED")
        self.assertEqual(severity, "HIGH")


if __name__ == "__main__":
    unittest.main()
