from ..utils.downloader import download_audio
from .voice_model import VoiceModel
from ..utils.config import TRAINING_DATA_BASE_DIR
from ..utils.logger import init as logger

logger = logger()
import pandas

def learn(tony_links_file: str, not_tony_links_file: str):
    voice_model = VoiceModel()
    tony_data = pandas.read_csv(tony_links_file)
    tony_data.fillna("", inplace=True)
    logger.info(f"Processing {tony_data.size} Tony Hinchcliffe YouTube links...")
    # Load Tony Hinchcliffe audio from a csv with possible cut times start and end
    for index, row in tony_data.iterrows():
        download_audio(row['link'], f"{TRAINING_DATA_BASE_DIR}/tony", row['ss'], row['to'])

    # Load "Not Tony Hinchcliffe" audio (just raw links, no need to cut videos of not tony)
    with open(not_tony_links_file, 'r') as f:
        not_tony_links = [line.strip() for line in f if line.strip()]
        logger.info(f"Processing {len(not_tony_links)} 'Not Tony Hinchcliffe' YouTube links...")
        for link in not_tony_links:
            download_audio(link, f"{TRAINING_DATA_BASE_DIR}/not_tony")

    voice_model.train(TRAINING_DATA_BASE_DIR)