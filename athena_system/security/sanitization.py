import re

class PIISanitizer:
    def __init__(self):
        # Regex patterns for common PII
        self.patterns = {
            "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b'
        }

    def redact(self, text):
        """
        Redacts PII from the input text.
        """
        redacted_text = text
        for pii_type, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", redacted_text)
        
        return redacted_text

if __name__ == "__main__":
    sanitizer = PIISanitizer()
    sample_text = "Contact John Doe at john.doe@example.com or call 555-123-4567 regarding the merger."
    print(f"Original: {sample_text}")
    print(f"Redacted: {sanitizer.redact(sample_text)}")
