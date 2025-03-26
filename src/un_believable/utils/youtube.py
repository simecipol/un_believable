import re
def extract_video_id(url: str) -> str:
    # Regex to match YouTube video URLs (regular & Shorts)
    pattern = (
        r"(?:https?://)?(?:www\.)?"
        r"(?:youtube\.com/(?:.*v=|shorts/)|youtu\.be/)"
        r"(?P<id>[a-zA-Z0-9_-]{11})"
    )
    
    match = re.search(pattern, url)
    return match.group("id") if match else None