from typing import Union
from contextlib import asynccontextmanager
import uvicorn
import tempfile
import os
import time
import base64

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.STTService import STTService
from services.MistralService import MistralService
from services.TTSService import TTSService
from services.CoquiService import CoquiService

# Variable globale pour le service STT
stt_service: STTService = None
mistral_service: MistralService = None
tts_service: TTSService = None
coqui_service: CoquiService = None
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise les services au démarrage de l'application"""
    global stt_service, mistral_service, tts_service, coqui_service
    print("🚀 Chargement du modèle Whisper...")
    stt_service = STTService(model_size="small", device="cpu")
    print("✅ Modèle chargé !")
    print("🚀 Chargement du modèle Mistral...")
    mistral_service = MistralService(model="mistral-medium-latest")
    print("✅ Modèle chargé !")
    print("🚀 Chargement du modèle TTS...")
    model_path = os.path.join(os.path.dirname(__file__), "services", "models", "mls", "fr_FR-mls-medium.onnx")
    tts_service = TTSService(model_path=model_path, use_cuda=False)
    print("✅ Modèle chargé !")
    print("🚀 Chargement du modèle Coqui...")
    coqui_service = CoquiService(model_name="tts_models/fr/css10/vits")
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

# CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        response = mistral_service.chat(text).choices[0].message.content
        
        # Générer l'audio et l'encoder en base64
        audio_bytes = tts_service.synthesize_to_bytes(response)
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        processing_time = time.time() - start_time
        print(response)
        
        return {
            "text": text,
            "response": response,
            "audio": audio_base64,
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