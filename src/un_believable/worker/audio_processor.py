import librosa
import numpy as np
from ..utils.logger import init as logger
logger = logger()
def extract_features(audio_path: str) -> np.ndarray:
    """Extracts audio features (MFCCs, Spectral Centroid, Spectral Contrast, Chroma Features) for speaker recognition."""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_centroid_mean = np.mean(spec_centroid.T, axis=0)
        spec_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spec_contrast_mean = np.mean(spec_contrast.T, axis=0)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma.T, axis=0)
        features = np.hstack([mfccs_mean, spec_centroid_mean, spec_contrast_mean, chroma_mean])
        return features
    except Exception as e:
        logger.error(f"Error extracting features from {audio_path}: {e}")
        return None
