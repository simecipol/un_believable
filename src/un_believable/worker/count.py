import os
import random
import string
from typing import Dict
from pydub import AudioSegment
from ..utils.config import AUDIO_SPLITS_BASE__DIR
from ..utils.logger import init as logger
from .phrase_detector import PhraseDetector
from .audio_processor import extract_features
from .voice_model import LABEL_TONY, VoiceModel

logger = logger()

def count(audio_path: str, hf_token: str) -> Dict:
    """Dizarizes and concats all tony segments into one wav, and counts the phrases in the transcription of it"""
    voice_model = VoiceModel()
    voice_model.load()
    phrase_detector = PhraseDetector(hf_token=hf_token)
    splits = phrase_detector.split_audio_by_speaker(audio_path)
    predictions = {}
    for speaker, file in splits.items():
        logger.info(f"Checking {file}'s probability of being Tony")
        features = extract_features(file)
        prediction, probability = voice_model.predict(features)
        logger.debug(f"{speaker}/{file}: {prediction}/{probability}")
        if prediction == LABEL_TONY:
            predictions[speaker] = probability

    if predictions:
        path = ""
        if len(predictions.items()) > 1:
            splits = [AudioSegment.from_wav(splits[k]) for k in predictions.keys()]
            combined = sum(splits)
            path = f"{AUDIO_SPLITS_BASE__DIR}/concat-{os.path.splitext(os.path.basename(audio_path))[0]}-{''.join(random.choices(string.ascii_letters, k=10))}.wav"
            logger.info(f"There are {len(predictions.items())} speakers with predictions to be tony. Joining them into {path}")
            combined.export(path, format="wav")
        else: 
            logger.info(f"The only positibe prediction to be tony is {next(iter(predictions))}")
            path = splits[next(iter(predictions))]
        return phrase_detector.count_phrases(path)
    return {}
