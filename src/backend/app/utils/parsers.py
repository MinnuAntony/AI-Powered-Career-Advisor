import re, json

def extract_json_from_text(text: str):
    """
    Extract JSON array from model text response, even if extra text or markdown surrounds it.
    """
    # Case 1: look for fenced JSON block
    match = re.search(r"```json\s*(\[.*?\])\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    
    # Case 2: find first [...] array in text
    match = re.search(r"(\[.*\])", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Case 3: try direct parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return []
