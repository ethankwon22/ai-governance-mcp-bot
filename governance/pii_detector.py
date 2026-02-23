# pii_detector.py - 개인정보(PII) 탐지
from governance.regex_rules import REGEX_RULES

def detect_pii_regex(text: str):
    findings = []
    for name, pattern in REGEX_RULES.items():
        matches = pattern.findall(text)
        if matches:
            findings.append({
                "type": name,
                "matches": matches
            })
    return findings

def contains_pii(text: str) -> bool:
    return len(detect_pii_regex(text)) > 0


if __name__ == "__main__":
    sample = "My email is john.doe@gmail.com and my SSN is 123-45-6789"
    print(detect_pii_regex(sample))