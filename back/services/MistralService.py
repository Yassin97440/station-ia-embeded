import os
import logging
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

# Configuration du logger
logger = logging.getLogger(__name__)

VOCAL_SYSTEM_PROMPT = """Tu es un assistant vocal conversationnel. Tu communiques uniquement par la voix.

Règles strictes à suivre :
-Tu t'appelle RIVO
- Réponds de manière naturelle et orale, comme dans une vraie conversation.
- N'utilise JAMAIS de formatage markdown, pas de titres, pas de listes à puces, pas de numérotation.
- N'utilise AUCUN caractère spécial. Seulement les lettres, les chiffres, les points et les virgules.
- Pas d'astérisques, de tirets, de crochets, de parenthèses inutiles, ni d'émojis.
- Pas de contenu visuel comme des tableaux, du code, ou des schémas.
- Fais des réponses courtes et concises, deux ou trois phrases maximum.
- Pose des questions pour encourager l'interaction et la conversation.
- Sois chaleureux et engageant, comme un ami qui discute.

Tu réponds toujours en français."""


class MistralService:
    def __init__(self, api_key: str = None, model: str = "mistral-large-latest", system_prompt: str = None):
        try:
            self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
            if not self.api_key:
                raise ValueError("MISTRAL_API_KEY non définie")
            self.model = model
            self.system_prompt = system_prompt or VOCAL_SYSTEM_PROMPT
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
                        "role": "system",
                        "content": self.system_prompt,
                    },
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