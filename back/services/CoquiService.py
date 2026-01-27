import os
import logging
import subprocess
import tempfile
from typing import Optional

# Configuration du logger
logger = logging.getLogger(__name__)


class CoquiService:
    """
    Client pour Coqui TTS via Docker (mode CLI).
    Exécute des commandes Docker pour synthétiser du texte en audio.
    """
    
    def __init__(
        self, 
        docker_image: str = "ghcr.io/coqui-ai/tts-cpu",
        model_name: str = "tts_models/fr/css10/vits",
        output_dir: str = None,
        use_cuda: bool = False
    ):
        """
        Initialise le service Coqui TTS.
        
        Args:
            docker_image: Image Docker à utiliser (défaut: ghcr.io/coqui-ai/tts-cpu)
            model_name: Nom du modèle TTS (défaut: tts_models/fr/css10/vits pour le français)
            output_dir: Répertoire de sortie pour les fichiers audio
            use_cuda: Utiliser GPU (nécessite ghcr.io/coqui-ai/tts au lieu de tts-cpu)
        """
        self.docker_image = docker_image
        self.model_name = model_name
        self.use_cuda = use_cuda
        
        # Répertoire de sortie par défaut
        if output_dir is None:
            self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tts-output")
        else:
            self.output_dir = output_dir
        
        # Créer le répertoire de sortie
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"CoquiService initialisé - Image: {self.docker_image}, Modèle: {self.model_name}")
    
    def synthesize_to_file(
        self, 
        text: str, 
        output_filename: str = "response.wav"
    ) -> str:
        """
        Synthétise du texte en fichier audio via Docker.
        
        Args:
            text: Texte à synthétiser
            output_filename: Nom du fichier de sortie (sera dans output_dir)
            
        Returns:
            Chemin absolu du fichier audio généré
            
        Raises:
            ValueError: Si le texte est vide
            subprocess.CalledProcessError: Si la commande Docker échoue
        """
        if not text or not text.strip():
            raise ValueError("Le texte ne peut pas être vide")
        
        logger.info(f"Synthèse TTS Coqui - texte: {len(text)} caractères")
        
        # Chemin de sortie
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Construire la commande Docker
        # Note: On monte le répertoire de sortie dans le conteneur
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{self.output_dir}:/output",
            self.docker_image,
            "--text", text,
            "--model_name", self.model_name,
            "--out_path", f"/output/{output_filename}"
        ]
        
        if self.use_cuda:
            cmd.insert(2, "--gpus")
            cmd.insert(3, "all")
        
        try:
            logger.debug(f"Commande Docker: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"Audio généré avec succès: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur Docker Coqui TTS: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("Docker n'est pas installé ou non accessible")
            raise
    
    def synthesize(self, text: str) -> bytes:
        """
        Synthétise du texte et retourne les bytes audio.
        
        Args:
            text: Texte à synthétiser
            
        Returns:
            Bytes audio WAV
        """
        # Utiliser un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_filename = os.path.basename(tmp.name)
        
        try:
            output_path = self.synthesize_to_file(text, tmp_filename)
            
            with open(output_path, "rb") as f:
                audio_bytes = f.read()
            
            return audio_bytes
        finally:
            # Nettoyer le fichier temporaire
            tmp_path = os.path.join(self.output_dir, tmp_filename)
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def synthesize_and_save(
        self, 
        text: str, 
        output_path: str = "response.wav"
    ) -> tuple[bytes, str]:
        """
        Synthétise du texte, sauvegarde sur disque ET retourne les bytes.
        
        Args:
            text: Texte à synthétiser (ex: réponse de Mistral)
            output_path: Chemin du fichier de sortie
            
        Returns:
            Tuple (bytes audio, chemin du fichier)
        """
        # Déterminer le nom du fichier et le répertoire
        if os.path.isabs(output_path):
            # Chemin absolu fourni - extraire le nom de fichier
            output_filename = os.path.basename(output_path)
            # Copier vers le chemin demandé après génération
            final_path = output_path
        else:
            output_filename = output_path
            final_path = os.path.join(self.output_dir, output_filename)
        
        # Générer l'audio
        generated_path = self.synthesize_to_file(text, output_filename)
        
        # Lire les bytes
        with open(generated_path, "rb") as f:
            audio_bytes = f.read()
        
        # Si le chemin final est différent, copier le fichier
        if final_path != generated_path:
            os.makedirs(os.path.dirname(final_path) or ".", exist_ok=True)
            with open(final_path, "wb") as f:
                f.write(audio_bytes)
            logger.info(f"Audio copié vers: {final_path}")
        
        logger.info(f"Audio synthétisé: {final_path} ({len(audio_bytes)} bytes)")
        return audio_bytes, final_path
    
    def list_models(self) -> str:
        """
        Liste les modèles TTS disponibles.
        
        Returns:
            Liste des modèles disponibles (stdout de la commande)
        """
        cmd = [
            "docker", "run", "--rm",
            self.docker_image,
            "--list_models"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de la liste des modèles: {e.stderr}")
            raise


# Exemple d'utilisation
# coqui = CoquiService(model_name="tts_models/fr/css10/vits")
# audio_bytes, file_path = coqui.synthesize_and_save("Bonjour, comment allez-vous?", "response.wav")
