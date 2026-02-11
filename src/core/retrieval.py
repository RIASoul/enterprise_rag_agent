from typing import List, Dict, Any
import re

from config import config

class RAGRetriever:
    """Système de récupération pour RAG"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
    
    def retrieve(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """Récupère les documents pertinents - VERSION SIMPLIFIÉE"""
        if k is None:
            k = config.TOP_K_RESULTS
        
        print(f"🔍 Recherche pour: '{query}'")
        
        try:
            # Recherche simple
            documents = self.vector_store.search(query, k)
            
            if not documents:
                print("⚠️ Aucun document trouvé")
                # Essayer avec une requête simplifiée
                simple_query = self._simplify_query(query)
                if simple_query != query:
                    print(f"🔄 Essai avec requête simplifiée: '{simple_query}'")
                    documents = self.vector_store.search(simple_query, k)
            
            if documents:
                print(f"✅ {len(documents)} documents récupérés")
                # Filtrer par score minimum
                filtered = [doc for doc in documents if doc.get('score', 0) >= 0.1]
                return filtered if filtered else documents[:2]  # Retourner au moins 2
            
            return []
            
        except Exception as e:
            print(f"❌ Erreur récupération: {e}")
            return []
    
    def _simplify_query(self, query: str) -> str:
        """Simplifie la requête"""
        if not query:
            return ""
        
        # Extraire les mots-clés
        words = re.findall(r'\b[a-zàâçéèêëîïôûùüÿæœ]+\b', query.lower())
        
        # Stop words
        stop_words = {'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 
                     'pour', 'avec', 'sur', 'dans', 'par', 'est', 'sont', 'qui', 'que'}
        
        # Garder les mots longs et significatifs
        keywords = [w for w in words if len(w) > 2 and w not in stop_words]
        
        # Prendre les 3-4 mots les plus longs
        keywords.sort(key=len, reverse=True)
        simplified = ' '.join(keywords[:4])
        
        return simplified if simplified else query[:50]
    
    def format_context(self, documents: List[Dict[str, Any]]) -> str:
        """Formate le contexte pour le modèle"""
        if not documents:
            return "Aucun document pertinent trouvé."
        
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            source = doc['metadata'].get('source', 'Document')
            chunk_id = doc['metadata'].get('chunk_id', '1')
            text = doc['text']
            
            # Format standard
            context_parts.append(f"[Document {i}: {source} (chunk {chunk_id})]")
            context_parts.append(text)
        
        return "\n".join(context_parts)
    
    def format_sources_for_display(self, documents: List[Dict[str, Any]]) -> str:
        """Formate les sources pour l'affichage"""
        if not documents:
            return "Aucune source"
        
        sources = []
        for i, doc in enumerate(documents, 1):
            source = doc['metadata'].get('source', 'Document')
            chunk_id = doc['metadata'].get('chunk_id', 'N/A')
            score = doc.get('score', 0.0)
            preview = doc['text'][:100] + "..." if len(doc['text']) > 100 else doc['text']
            
            sources.append(f"**{i}. {source}** (section {chunk_id}, score: {score:.2f})\n{preview}")
        
        return "\n\n".join(sources)