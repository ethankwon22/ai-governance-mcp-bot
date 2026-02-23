# presidio_wrapper.py - Presidio 래퍼(선택 사용)
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def detect_pii_presidio(text: str):
    results = analyzer.analyze(text=text, language="en")
    findings = []
    for r in results:
        findings.append({
            "entity_type": r.entity_type,
            "start": r.start,
            "end": r.end,
            "score": round(r.score, 3)
        })
    return findings

def anonymize_text(text: str):
    results = analyzer.analyze(text=text, language="en")
    return anonymizer.anonymize(text=text, analyzer_results=results).text


if __name__ == "__main__":
    sample = "My name is John Doe and I live in Pittsburgh. Email me at john.doe@gmail.com"
    print(detect_pii_presidio(sample))
    print(anonymize_text(sample))