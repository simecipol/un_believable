# un_believable/src/un_believable/cli.py
import json
import click
import time

from .utils.config import COUNT_DOWNLOAD_DATA_BASE_DIR
from .utils.downloader import download_audio
from .worker.learn import learn as worker_learn
from .youtube.main import post_comment, extract_video_id
from .worker.count import count as worker_count
from .utils.db import Episode, Comment, write, init_db
from .utils.logger import init as logger
from .reddit.main import post as post_to_reddit
logger = logger()

@click.group()
def main():
    """A poetry project to recognize Tony Hinchcliffe's voice and catchphrases."""
    pass

@main.command()
@click.option('--tony-links-file', type=click.Path(exists=True), help='Path to a file containing YouTube links of Tony Hinchcliffe.')
@click.option('--not-tony-links-file', type=click.Path(exists=True), help='Path to a file containing YouTube links of other speakers.')
def learn(tony_links_file, not_tony_links_file):
    """Downloads audio and trains the voice model."""
    # worker_learn(tony_links_file, not_tony_links_file)
    logger.info("Disabled intentionally due to a good model training outcome")

@main.command()
@click.option('--youtube-link', type=str, required=True, help='The YouTube Short link to analyze.')
@click.option('--hf-token', type=str, required=True, default=None, help='Your Hugging Face access token for diarization.')
def count(youtube_link, hf_token):
    """Downloads audio from a YouTube Short, attempts diarization, and counts catchphrases per speaker."""
    audio_path = download_audio(youtube_link, output_dir=COUNT_DOWNLOAD_DATA_BASE_DIR)
    tony_counts = worker_count(audio_path, hf_token)
    st = time.time()
    if tony_counts:
        init_db()
        episode = write(Episode(
            title="TBD",
            video_id=extract_video_id(youtube_link),
            is_validation=False,
            **{k.replace(" ", "_"): v for k, v in tony_counts.items()}
        ))
        comment_youtube_id, episode_name = post_comment(youtube_link, tony_counts)
        post_to_reddit(tony_counts, episode_name, youtube_link)
        logger.info(json.dumps(tony_counts))
        logger.info(f"Total time {time.time() - st} seconds.")
