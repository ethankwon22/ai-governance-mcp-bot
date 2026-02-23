from governance.regex_rules import REGEX_RULES
from governance.presidio_wrapper import detect_pii_presidio

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

def detect_pii_hybrid(text: str):
    regex_hits = detect_pii_regex(text)
    presidio_hits = detect_pii_presidio(text)

    return {
        "regex": regex_hits,
        "presidio": presidio_hits
    }

def contains_pii(text: str) -> bool:
    results = detect_pii_hybrid(text)
    return bool(results["regex"] or results["presidio"])


if __name__ == "__main__":
    sample = "My name is John Doe. My email is john.doe@gmail.com"
    print(detect_pii_hybrid(sample))