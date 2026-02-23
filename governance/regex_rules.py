# regex_rules.py - 정규식 기반 규칙(민감정보 등)
import re

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"\+?\d{1,2}[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}")
SSN_REGEX = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

REGEX_RULES = {
    "email": EMAIL_REGEX,
    "phone": PHONE_REGEX,
    "ssn": SSN_REGEX,
}