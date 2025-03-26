import json
import google_auth_oauthlib.flow
import googleapiclient.discovery

from ..utils.youtube import extract_video_id
from ..utils.logger import init as logger

logger = logger()
# Set up OAuth 2.0 authentication
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def generate_comment(phrase_counts: dict) -> str:
    phrases = [f'"{phrase}" said {count} times' for phrase, count in phrase_counts.items() if count > 0]
    
    if not phrases:
        return "Tony must've been on his best behavior this episode... suspicious. 🤔"

    comment = [
        "🔥 Kill Tony Un-believable Bot is in the house! 🔥",
        "Here's a Tony-isms breakdown for this episode:",
        "",
        "\n".join(f"✅ {p}" for p in phrases),
        "",
        "If Tony says it, I count it. If I miss one, you're too sober. 🍻"
    ]

    return "\n".join(comment)

def authenticate_youtube():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def post_comment(video_url, phrase_counts):
    youtube = authenticate_youtube()
    comment_text = generate_comment(phrase_counts=phrase_counts)
    video_id = extract_video_id(video_url)
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    )
    response = request.execute()
    logger.info("Comment posted:", response)
    comment_id = response["id"]
    # Get the video title
    request = youtube.videos().list(
        part="snippet",  
        id=video_id
    )
    response = request.execute()
    # Extract and return the title
    title = ""
    if "items" in response and response["items"]:
        title = response["items"][0]["snippet"]["title"]
    return comment_id, title
