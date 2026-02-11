import os
import requests
from typing import List, Dict

class OllamaModel:
    """LLM local via Ollama"""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "llama3:8b")
        self.base_url = os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434/api/generate"
        )

    def generate_response(
        self,
        query: str,
        context: str = "",
        conversation_history: List[Dict[str, str]] = None
    ) -> str:

        system_prompt = (
            "Tu es un assistant conversationnel d'entreprise.\n"
            "Tu dois répondre STRICTEMENT à partir du contexte fourni.\n\n"
            "RÈGLES:\n"
            "1. Ne jamais inventer d'information\n"
            "2. Si l'information n'est pas dans le contexte, dis-le clairement\n"
            "3. Réponse professionnelle, claire et concise\n"
        )

        prompt = system_prompt

        if context:
            prompt += f"\nCONTEXTE:\n{context}\n"

        if conversation_history:
            for msg in conversation_history[-3:]:
                role = msg.get("role", "").upper()
                content = msg.get("content", "")
                prompt += f"\n{role}: {content}"

        prompt += f"\n\nQUESTION: {query}\nRÉPONSE:"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 4096
            }
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip() or \
                "Je ne trouve pas l'information dans les documents fournis."
        except Exception as e:
            return f"Erreur Ollama : {str(e)}"
