import re

def parse_ai_response(content: str):
    # Strip the "Athena (GM):" prefix to clean the output
    clean_text = re.sub(r'Athena \(GM\):', '', content, flags=re.IGNORECASE).strip()
    
    image_match = re.search(r'<<IMAGE:(.*?)>>', clean_text)
    image_tag = image_match.group(1) if image_match else None
    
    clean_text = re.sub(r'<<IMAGE:.*?>>', '', clean_text).strip()
    return clean_text, image_tag