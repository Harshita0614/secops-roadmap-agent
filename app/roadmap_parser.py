#reads secops sow pdf
#extracts roadmap/services phases and tasks
#return a clean list of steps 

import fitz  # PyMuPDF

def get_roadmap_steps(pdf_path: str) -> list:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Basic keyword-based section detection (customize as needed)
    sections = []
    keywords = ["Validation", "Integration", "Detection", "Use Case", "SOAR", "Playbook", "Fine-tuning"]

    for line in text.splitlines():
        for word in keywords:
            if word.lower() in line.lower() and len(line.strip()) > 10:
                sections.append(line.strip())
                break

    # Remove duplicates while preserving order
    unique_steps = []
    [unique_steps.append(step) for step in sections if step not in unique_steps]

    return unique_steps
