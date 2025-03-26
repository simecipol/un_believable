import os
import numpy as np
from sklearn.model_selection import train_test_split
from ..utils.config import VOICE_MODEL_PATH, TRAINING_DATA_BASE_DIR
from .audio_processor import extract_features
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from ..utils.logger import init as logger

logger = logger()

LABEL_TONY = 'tony'
LABEL_NOT_TONY = 'not_tony'

def build_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

class VoiceModel:
    def __init__(self):
        self.model_path = VOICE_MODEL_PATH
        self.model = None

    def train(self, training_data_dir: str = TRAINING_DATA_BASE_DIR):
        all_features = []
        all_labels = []
        
        for label in os.listdir(training_data_dir):
            if label in [LABEL_TONY, LABEL_NOT_TONY]:
                label_dir = os.path.join(training_data_dir, label)
                if os.path.isdir(label_dir):
                    for file in os.listdir(label_dir):
                        file_path = os.path.join(label_dir, file)
                        features = extract_features(file_path)
                        if features is not None:
                            all_features.append(features)
                            all_labels.append(1 if label == LABEL_TONY else 0)
        
        X = np.array(all_features)
        y = np.array(all_labels)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        self.model = build_model(input_shape=(X_train.shape[1],))
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=120, batch_size=16)
        self.model.save(self.model_path)
        logger.info(f"Model trained and saved as {self.model_path}.")


    def load(self):
        """Loads the trained voice recognition model."""
        self.model = load_model(self.model_path)
        logger.info(f"Voice model loaded from {self.model_path}")

    def predict(self, feature: np.ndarray) -> tuple[str, float]:
        """Predicts the speaker of the given audio features."""
        feature = np.expand_dims(feature, axis=0)
        if self.model and feature is not None:
            probability = self.model.predict(feature)[0][0]
            prediction = LABEL_TONY if probability >= 0.51 else LABEL_NOT_TONY
            return prediction, probability
        else:
            return "Unknown", 0.0
