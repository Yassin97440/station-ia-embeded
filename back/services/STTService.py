from faster_whisper import WhisperModel
from typing import Tuple
import io

class STTService:
    """Service de Speech-to-Text avec Faster-Whisper"""
    
    def __init__(self, model_size: str = "base", device: str = "cpu"):
        compute_type = "float16" if device == "cuda" else "int8"
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    def transcribe(self, audio_path: str, language: str = "fr") -> Tuple[str, dict]:
        """
        Transcrit un fichier audio en texte.
        
        Args:
            audio_path: Chemin vers le fichier audio
            language: Code langue (fr, en, etc.)
            
        Returns:
            Tuple (texte, métadonnées)
        """
        segments, info = self.model.transcribe(audio_path, language=language)
        text = " ".join([s.text for s in segments]).strip()
        
        metadata = {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration
        }
        
        return text, metadata

# Test
# stt = STTService(model_size="base")
# text, meta = stt.transcribe("test.wav")
# print(text, meta)