import os
import logging
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

# Configuration du logger
logger = logging.getLogger(__name__)

class MistralService:
    def __init__(self, api_key: str = None, model: str = "mistral-medium-latest"):
        try:
            self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
            if not self.api_key:
                raise ValueError("MISTRAL_API_KEY non définie")
            self.model = model
            self.client = Mistral(api_key=self.api_key)
            logger.info("MistralService initialisé avec succès")
        except ValueError as e:
            logger.error(f"Erreur de configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client Mistral: {e}")
            raise

    def chat(self, message: str) -> str:
        try:
            if not message or not message.strip():
                raise ValueError("Le message ne peut pas être vide")
            
            logger.info(f"Envoi d'un message à Mistral (longueur: {len(message)} caractères)")
            
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    },
                ]
            )
            
            logger.info("Réponse reçue de Mistral avec succès")
            return response
            
        except ValueError as e:
            logger.error(f"Erreur de validation: {e}")
            raise
        except ConnectionError as e:
            logger.error(f"Erreur de connexion à l'API Mistral: {e}")
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue lors de l'appel à Mistral: {e}")
            raise

# Test
# print(chat_with_mistral("What is the best French cheese?"))