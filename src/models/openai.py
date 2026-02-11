import os
from openai import OpenAI
from typing import List, Dict


class OpenAIModel:
    """
    Modèle OpenAI (ChatGPT) pour projet RAG
    Compatible Streamlit / FastAPI
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.temperature = float(os.getenv("TEMPERATURE", 0.1))
        self.max_tokens = int(os.getenv("MAX_TOKENS", 2048))

    def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Génère une réponse à partir du contexte RAG + historique
        """

        system_prompt = (
            "You are an enterprise-grade AI assistant.\n"
            "Answer ONLY using the provided context.\n"
            "If the answer is not in the context, say clearly that you do not know.\n"
            "Be concise, professional, and factual."
        )

        messages = [{"role": "system", "content": system_prompt}]

        # Historique (optionnel)
        if conversation_history:
            for msg in conversation_history[-6:]:  # limiter l'historique
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Message principal avec contexte RAG
        user_prompt = f"""
CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""
        messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return response.choices[0].message.content.strip()

    def _no_documents_response(self, query: str) -> str:
        return (
            "⚠️ Aucun document n'est disponible pour répondre à votre question.\n\n"
            "Veuillez d'abord charger des documents."
        )
