from piper import PiperVoice
from typing import Optional, Generator
import wave
import io
import os


class TTSService:
    """Service de Text-to-Speech avec Piper TTS"""
    
    def __init__(self, model_path: str, use_cuda: bool = False):
        """
        Initialise le service TTS avec un modèle Piper.
        
        Args:
            model_path: Chemin vers le fichier .onnx du modèle de voix
            use_cuda: Utiliser GPU CUDA pour l'accélération (nécessite onnxruntime-gpu)
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modèle de voix non trouvé: {model_path}")
        
        self.voice = PiperVoice.load(model_path, use_cuda=use_cuda)
        self.model_path = model_path
    
    def synthesize_to_file(
        self, 
        text: str, 
        output_path: str,
        volume: float = 1.0,
        speed: float = 1.0,
        noise_scale: float = 0.667,
        noise_w_scale: float = 0.8
    ) -> str:
        """
        Synthétise du texte en fichier audio WAV.
        
        Args:
            text: Texte à synthétiser
            output_path: Chemin du fichier WAV de sortie
            volume: Volume (0.0 à 1.0+)
            speed: Vitesse (1.0 = normal, 2.0 = 2x plus lent)
            noise_scale: Variation audio (0.0 à 1.0)
            noise_w_scale: Variation de parole (0.0 à 1.0)
            
        Returns:
            Chemin du fichier audio généré
        """
        from piper.voice import SynthesisConfig
        
        syn_config = SynthesisConfig(
            volume=volume,
            length_scale=speed,
            noise_scale=noise_scale,
            noise_w_scale=noise_w_scale
        )
        
        with wave.open(output_path, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file, syn_config=syn_config)
        
        return output_path
    
    def synthesize_to_bytes(
        self, 
        text: str,
        volume: float = 1.0,
        speed: float = 1.0,
        noise_scale: float = 0.667,
        noise_w_scale: float = 0.8
    ) -> bytes:
        """
        Synthétise du texte en bytes audio WAV (pour réponse HTTP directe).
        
        Args:
            text: Texte à synthétiser
            volume: Volume (0.0 à 1.0+)
            speed: Vitesse (1.0 = normal, 2.0 = 2x plus lent)
            noise_scale: Variation audio
            noise_w_scale: Variation de parole
            
        Returns:
            Bytes du fichier WAV
        """
        from piper.voice import SynthesisConfig
        
        syn_config = SynthesisConfig(
            volume=volume,
            length_scale=speed,
            noise_scale=noise_scale,
            noise_w_scale=noise_w_scale
        )
        
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file, syn_config=syn_config)
        
        buffer.seek(0)
        return buffer.read()
    
    def synthesize_stream(
        self, 
        text: str
    ) -> Generator[bytes, None, None]:
        """
        Synthétise du texte en streaming (chunks audio).
        Utile pour des réponses temps réel.
        
        Args:
            text: Texte à synthétiser
            
        Yields:
            Chunks de bytes audio bruts (int16)
        """
        for chunk in self.voice.synthesize(text):
            yield chunk.audio_int16_bytes


# Test
# tts = TTSService("path/to/fr_FR-siwis-medium.onnx")
# tts.synthesize_to_file("Bonjour, comment allez-vous?", "output.wav")
# audio_bytes = tts.synthesize_to_bytes("Test de synthèse vocale")
