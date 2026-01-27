from piper import PiperVoice
from typing import Optional, Generator
import wave
import io
import os
import re
import unicodedata


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
            self.voice.synthesize_wav(normalize_text_for_tts(text), wav_file, syn_config=syn_config)
        
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
            self.voice.synthesize_wav(normalize_text_for_tts(text), wav_file, syn_config=syn_config)
        
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

def normalize_text_for_tts(text: str) -> str:
    if not text:
        return ""

    # 1. Normalisation unicode (supprime caractères bizarres)
    text = unicodedata.normalize("NFKC", text)

    # 2. Supprimer les retours à la ligne
    text = text.replace("\n", " ").replace("\r", " ")

    # 3. Remplacer ponctuation agressive par des points
    text = text.replace("?", ".").replace("!", ".")

    # 4. Supprimer tout caractère non souhaité
    # (lettres, chiffres, espace, point, virgule, apostrophe simple)
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s\.,']", " ", text)

    # 5. Réduire les espaces multiples
    text = re.sub(r"\s+", " ", text)

    # 6. Découper les phrases trop longues
    sentences = re.split(r"\.", text)
    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Coupe les phrases trop longues (≈ 20 mots max)
        words = sentence.split(" ")
        while len(words) > 20:
            chunk = words[:20]
            clean_sentences.append(" ".join(chunk))
            words = words[20:]

        if words:
            clean_sentences.append(" ".join(words))

    # 7. Recomposer avec des points
    text = ". ".join(clean_sentences)

    # 8. Nettoyage final
    text = text.strip(" .") + "."

    return text
# Test
# tts = TTSService("path/to/fr_FR-siwis-medium.onnx")
# tts.synthesize_to_file("Bonjour, comment allez-vous?", "output.wav")
# audio_bytes = tts.synthesize_to_bytes("Test de synthèse vocale")
