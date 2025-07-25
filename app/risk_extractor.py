#read uploaded .eml email files 
#extract potential risks,blockers, or delays

import os
from email import policy
from email.parser import BytesParser

def extract_email_text(eml_path: str) -> str:
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                body += part.get_content()
    else:
        body = msg.get_content()

    return body

def get_risks(eml_paths: list) -> dict:
    keywords = ['blocked', 'delay', 'pending', 'issue', 'risk', 'concern', 'incomplete']
    risk_map = {}

    for path in eml_paths:
        text = extract_email_text(path)
        for line in text.splitlines():
            if any(k in line.lower() for k in keywords):
                for phase in ['SOAR', 'Playbook', 'Use Case', 'SIEM', 'Detection', 'Integration']:
                    if phase.lower() in line.lower():
                        risk_map.setdefault(phase, []).append(line.strip())

    return risk_map
