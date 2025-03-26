import os
import os.path
import subprocess
from .config import AUDIO_OUTPUT_DIR
import soundfile as sf
from ..utils.youtube import extract_video_id
from ..utils.logger import init as logger

logger = logger()

def download_audio(youtube_url: str, output_dir: str=AUDIO_OUTPUT_DIR, ss: str = "", to: str = "") -> str:
    """Downloads the audio from a YouTube video/short using yt-dlp and saves it as a WAV file."""
    os.makedirs(output_dir, exist_ok=True)
    id = extract_video_id(youtube_url)
    output_base = os.path.join(output_dir, id)
    output_wav = f"{output_base}.wav"
    if os.path.exists(output_wav):
        logger.info(f"Skipping download of {output_wav}, already exists.")
        return output_wav
    else:
        postprocessor_args = ""
        if ss != "":
            postprocessor_args += f"-ss {ss} "
        if to != "":
            postprocessor_args += f"-to {to} "

        try:
            command = [
                "yt-dlp",
                "-x",
                "--audio-format", "wav",
                "-f",
                "bestaudio",
                # "--postprocessor-args" if postprocessor_args != "" else "",
                # f"'{postprocessor_args}'" if postprocessor_args != "" else "",
                "-o", output_wav,
                youtube_url,
            ]
            logger.debug(f"Executing: {' '.join(command)}")
            subprocess.run(command, check=True, capture_output=True)

            return output_wav
        except subprocess.CalledProcessError as e:
            logger.info(f"Error downloading {youtube_url} with yt-dlp: {e.stderr.decode()}")
            return None
        except FileNotFoundError:
            logger.info("Error: yt-dlp is not installed or not in your system's PATH.")
            return None
        except Exception as e:
            logger.info(f"An unexpected error occurred while downloading or processing {youtube_url}: {e}")
            return None