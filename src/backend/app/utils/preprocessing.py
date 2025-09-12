from typing import Dict

def normalize_grades(grades: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize student grades to percentage (0–100).
    If grades are already in 0–100, this just returns them.
    """
    normalized = {}
    for subject, score in grades.items():
        if score <= 10:  # assume GPA scale (0–10)
            normalized[subject] = score * 10
        elif score <= 4:  # assume CGPA (0–4 scale)
            normalized[subject] = (score / 4) * 100
        else:
            normalized[subject] = score  # already percentage
    return normalized

def analyze_strengths(grades: Dict[str, float]) -> Dict[str, str]:
    """
    Classify each subject as Strong / Moderate / Weak.
    """
    strengths = {}
    for subject, score in grades.items():
        if score >= 80:
            strengths[subject] = "Strong"
        elif score >= 60:
            strengths[subject] = "Moderate"
        else:
            strengths[subject] = "Weak"
    return strengths
