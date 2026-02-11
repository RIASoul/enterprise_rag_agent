class FallbackModel:
    """Modèle de secours intelligent – VERSION STABLE"""

    def __init__(self):
        print("✅ Modèle de secours intelligent initialisé")
        self.cache = {}

    def generate_response(
        self,
        query: str,
        context: str = "",
        conversation_history=None
    ) -> str:
        query = query.strip()
        query_lower = query.lower()

        # 1️⃣ Salutations simples
        if query_lower in ["salut", "bonjour", "hello", "hi", "coucou"]:
            return (
                "👋 Bonjour !\n\n"
                "Je suis votre **assistant documentaire d’entreprise (mode démo)**.\n\n"
                "📄 Posez-moi une question liée à vos documents chargés."
            )

        # 2️⃣ Aide
        if any(word in query_lower for word in ["aide", "comment", "utiliser", "support"]):
            return self._help_response()

        # 3️⃣ Pas de contexte exploitable
        if not context or len(context.strip()) < 30:
            return (
                "⚠️ Je n’ai pas trouvé d’information exploitable dans les documents.\n\n"
                "👉 Essayez une question plus précise liée au contenu chargé."
            )

        # 4️⃣ Cache
        cache_key = f"{query_lower}_{hash(context[:200])}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 5️⃣ Réponse basée sur le contexte
        response = (
            "📄 **Réponse basée sur vos documents internes :**\n\n"
            f"{context[:1200]}...\n\n"
            "ℹ️ *(Mode démo – réponse extraite directement des documents)*"
        )

        self.cache[cache_key] = response
        return response

    def _help_response(self) -> str:
        return (
            "🤖 **Assistant documentaire d’entreprise**\n\n"
            "**Ce que je peux faire :**\n"
            "• Répondre à des questions sur les documents chargés\n"
            "• Expliquer des politiques internes\n"
            "• Résumer des procédures\n\n"
            "**Exemples :**\n"
            "• Quelle est la politique RH ?\n"
            "• Quelles sont les règles de sécurité ?\n"
            "• Quels sont les objectifs du code de conduite ?"
        )

    def _no_documents_response(self, query: str) -> str:
        return (
            "📚 **Aucun document chargé**\n\n"
            "Veuillez d’abord importer des documents pour pouvoir poser des questions."
        )
