
from collections import defaultdict
from temporalio import activity
import json

from ..utils.config import AUDI_TRANSCRIPTION_BASE_DIR, CATCHPHRASES, COUNT_DOWNLOAD_DATA_BASE_DIR
from ..utils.downloader import download_audio
from ..worker.phrase_detector import PhraseDetector
from ..worker.voice_model import VoiceModel

from ..youtube.main import post_comment
from ..reddit.main import post as post_to_reddit



@activity.defn
async def download(youtube_link: str):
    """Downloads audio from a YouTube Short, attempts diarization, and counts catchphrases per speaker."""
    file_path = download_audio(youtube_link, output_dir=COUNT_DOWNLOAD_DATA_BASE_DIR)
    return file_path

@activity.defn
async def split_audio_by_speaker(file: str):
    phrase_detector = PhraseDetector()
    splits = phrase_detector.split_audio_by_speaker(file)
    return splits

@activity.defn
async def tony_voice_detection(splits: dict, video_id: str):
    voice_model = VoiceModel()
    path = voice_model.find_and_merge_tony(splits=splits, id=video_id)
    return path

@activity.defn
async def transcription(path: str, video_id: str):
    phrase_detector = PhraseDetector()
    output_file = f"{AUDI_TRANSCRIPTION_BASE_DIR}/{video_id}"
    phrase_detector.transcribe(path, output_file)
    return output_file

@activity.defn
async def phrase_counting(transcription_file: str):
    with open(transcription_file, 'r') as fp:
        transcription_dict = json.load(fp)
    phrase_counts_by_speaker = defaultdict(int)
    for segment in transcription_dict.get('segments', []):
        transcribed_text = segment.get('text', '').lower() 
        for phrase in CATCHPHRASES:
            phrase_counts_by_speaker[phrase] += transcribed_text.count(phrase.lower())
    return phrase_counts_by_speaker

@activity.defn
async def yt_comment(youtube_link: str, tony_counts: dict):
        return post_comment(youtube_link, tony_counts)

@activity.defn
async def reddit_post(youtube_link: str, tony_counts: dict, episode_name: str):
        post_to_reddit(tony_counts, episode_name, youtube_link)
