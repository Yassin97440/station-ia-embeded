from typing import Union
from contextlib import asynccontextmanager
import uvicorn
import tempfile
import os
import time

from fastapi import FastAPI, UploadFile, File, HTTPException

from services.STTService import STTService

# Variable globale pour le service STT
stt_service: STTService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise les services au démarrage de l'application"""
    global stt_service
    print("🚀 Chargement du modèle Whisper...")
    stt_service = STTService(model_size="small", device="cpu")
    print("✅ Modèle chargé !")
    yield
    # Cleanup si nécessaire
    print("👋 Arrêt de l'application")


app = FastAPI(
    title="Station IA - Assistant Vocal",
    description="API pour assistant vocal IA (STT → LLM → TTS)",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Station IA API"}


# ============== API v1 ==============

@app.post("/api/v1/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """
    Transcrit un fichier audio en texte.
    
    - **audio**: Fichier audio (WAV, MP3, M4A, etc.)
    
    Retourne le texte transcrit et les métadonnées.
    """
    if stt_service is None:
        raise HTTPException(status_code=503, detail="Service STT non initialisé")
    
    # Récupérer l'extension du fichier
    _, ext = os.path.splitext(audio.filename or ".wav")
    
    # Sauvegarder le fichier temporairement (faster-whisper a besoin d'un chemin)
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name
    
    try:
        start_time = time.time()
        text, metadata = stt_service.transcribe(tmp_path)
        processing_time = time.time() - start_time
        
        return {
            "text": text,
            "language": metadata["language"],
            "duration": metadata["duration"],
            "processing_time": round(processing_time, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transcription: {str(e)}")
    finally:
        # Nettoyer le fichier temporaire
        os.unlink(tmp_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)