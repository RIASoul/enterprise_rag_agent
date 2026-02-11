import os
from typing import List, Dict, Optional

from google import genai
from google.genai import types

from config import config


class GeminiModel:
    """Wrapper Gemini via Google GenAI SDK (stable)"""

    def __init__(self):
        api_key = (
            getattr(config, "GEMINI_API_KEY", None)
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )
        if not api_key:
            raise ValueError("GEMINI_API_KEY non configurée dans .env")

        self.client = genai.Client(api_key=api_key)
        self.model_name = getattr(config, "MODEL_NAME", "gemini-2.5-flash")
        self.last_error: Optional[str] = None

    def generate_response(
        self,
        query: str,
        context: str = "",
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        self.last_error = None

        # Salutations simples (évite un appel API inutile)
        q = (query or "").strip().lower()
        if q in {"bonjour", "salut", "hello", "hi", "coucou"}:
            return "Bonjour. Posez-moi une question liée aux documents chargés."

        # RAG strict : si pas de contexte, réponse contrôlée
        if not context or len(context.strip()) < 30:
            return "Je ne trouve pas cette information dans les documents disponibles."

        # Sécurité : tronquer le contexte pour éviter des erreurs de taille
        # (tu peux ajuster 12000 selon tes docs)
        if len(context) > 12000:
            context = context[:12000] + "\n\n[... contexte tronqué ...]"

        system_prompt = (
            "Tu es un assistant conversationnel d'entreprise.\n"
            "Tu dois répondre STRICTEMENT à partir du CONTEXTE fourni.\n\n"
            "RÈGLES:\n"
            "1) Ne jamais inventer d'information\n"
            "2) Si l'information n'est pas dans le contexte, dis: "
            "\"Je ne trouve pas cette information dans les documents disponibles.\"\n"
            "3) Réponse professionnelle, claire et concise\n"
        )

        prompt = system_prompt + "\n\n"
        prompt += f"CONTEXTE:\n{context}\n\n"

        if conversation_history:
            for msg in conversation_history[-3:]:
                role = (msg.get("role") or "").upper()
                content = msg.get("content") or ""
                prompt += f"{role}: {content}\n"

        prompt += f"\nQUESTION: {query}\nRÉPONSE:"

        try:
            cfg = types.GenerateContentConfig(
                temperature=getattr(config, "TEMPERATURE", 0.1),
                max_output_tokens=getattr(config, "MAX_TOKENS", 2048),
                top_p=0.95,
                top_k=40,
            )

            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=cfg,
            )

            text = (getattr(resp, "text", None) or "").strip()
            return text or "Je ne trouve pas cette information dans les documents disponibles."

        except Exception as e:
            self.last_error = str(e)
            return "Je suis désolé, une erreur technique est survenue. Veuillez réessayer."
