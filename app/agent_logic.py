""" this module will
-get the roadmap steps
-match each with current status
-inject known risks
-recommend:
 the current step 
 the next step
 risks to resolve 
 suggestions"""
from app.roadmap_parser import get_roadmap_steps
from app.status_tracker import get_step_status
from app.risk_extractor import get_risks
import difflib
def run_agent(pdf_path, xlsx_path, eml_paths):
    from app.roadmap_parser import get_roadmap_steps
    from app.status_tracker import get_step_status
    from app.risk_extractor import get_risks
    import difflib

    roadmap = get_roadmap_steps(pdf_path)
    status = get_step_status(xlsx_path)
    risks = get_risks(eml_paths)

    current_step = None
    for step in roadmap:
        closest = difflib.get_close_matches(step, status.keys(), n=1, cutoff=0.4)
        if closest:
            s = status[closest[0]]
            if s.lower() in ["in progress", "not valid", "pending"]:
                current_step = step
                break

    next_step = None
    if current_step:
        try:
            idx = roadmap.index(current_step)
            if idx + 1 < len(roadmap):
                next_step = roadmap[idx + 1]
        except ValueError:
            pass

    step_risks = {}
    for step in roadmap:
        for key in risks:
            if key.lower() in step.lower():
                step_risks[step] = risks[key]

    return {
        "roadmap": roadmap,
        "current": current_step,
        "next": next_step,
        "status": status.get(current_step, "Unknown"),
        "risks": step_risks.get(current_step, []),
        "suggestions": [
            "Escalate pending items",
            "Schedule a checkpoint meeting",
            "Review prerequisites for the next phase"
        ]
    }
