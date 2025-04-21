import json
import os
import time
import torch
import torchaudio
import whisperx

from ..utils.config import CATCHPHRASES, AUDIO_SPLITS_BASE__DIR
import soundfile as sf
from ..utils.logger import init
from collections import defaultdict
from ..utils.logger import init as logger

logger = logger()

class PhraseDetector:
    def __init__(self, model_name="large-v2", device="cpu", compute_type="float32", hf_token=os.getenv("HF_TOKEN", "")):
        self.stt_model = whisperx.load_model(model_name, device, compute_type=compute_type)
        self.diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)

    def transcribe(self, file_path: str, output_path: str = ""):
        st = time.time()
        audio = whisperx.load_audio(file_path)
        logger.info("Starting transcription. This may take a while...")
        result = self.stt_model.transcribe(audio)
        logger.debug(f"Transcription complete. Took: {time.time()-st} seconds.")
        if output_path != "":
            logger.info(f"Saving output of transcription to {output_path}")
            with open(output_path, 'w') as fp:
                json.dump(result, fp)
        return result

    def count_phrases(self, audio_path: str) -> dict[str, dict[str, int]]:
        """Transcribes the audio with diarization and counts catchphrases per speaker."""
        result = self.transcribe(file_path=audio_path)
        phrase_counts_by_speaker = defaultdict(int)
        logger.info("Starting to count phrases.")
        for segment in result.get('segments', []):
            transcribed_text = segment.get('text', '').lower() 
            for phrase in CATCHPHRASES:
                phrase_counts_by_speaker[phrase] += transcribed_text.count(phrase.lower())
        return phrase_counts_by_speaker

    def split_audio_by_speaker(self, audio_path):
        st = time.time()
        waveform, sample_rate = torchaudio.load(audio_path)
        audio = whisperx.load_audio(audio_path)
        logger.info("Starting diarization. This may take a while...")
        diarization_result = self.diarize_model(audio, min_speakers=10)
        speaker_audio = {}
        splits = {}
        for _, row in diarization_result.iterrows():
            speaker = row["speaker"]
            start, end = row["start"], row["end"]
            start_sample, end_sample = int(start * sample_rate), int(end * sample_rate)
            segment_audio = waveform[:, start_sample:end_sample]
            if speaker not in speaker_audio:
                speaker_audio[speaker] = [segment_audio]
            else:
                speaker_audio[speaker].append(segment_audio)
        for speaker, segments in speaker_audio.items():
            speaker_waveform = torch.cat(segments, dim=1)
            speaker_waveform = speaker_waveform.squeeze().T.numpy().astype("float32")  
            base_dir = f"{AUDIO_SPLITS_BASE__DIR}/{os.path.splitext(os.path.basename(audio_path))[0]}"
            output_path = os.path.join(base_dir, f"{speaker}.wav")
            os.makedirs(base_dir, exist_ok=True)
            sf.write(output_path, speaker_waveform, sample_rate, format="WAV", subtype="PCM_16")
            logger.debug(f"Saved {output_path}")
            splits[speaker] = output_path

        logger.info(f"Diarization complete. Took: {time.time() - st} seconds.")
        return splits
