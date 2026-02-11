import os
import chromadb
from typing import List, Dict, Any
import warnings

from config import config

# Supprimer les warnings
warnings.filterwarnings("ignore")

class VectorStore:
    """Vector Store simplifié"""
    
    def __init__(self):
        self.embedding_function = None  # ChromaDB gérera les embeddings
        self.collection_name = "documents"
        self._init_simple_chroma()
    
    def _init_simple_chroma(self):
        """Initialisation ChromaDB simplifiée"""
        print("🔄 Initialisation ChromaDB...")
        
        # Supprimer le dossier existant s'il y a un problème
        if os.path.exists(config.VECTOR_STORE_PATH):
            try:
                import shutil
                shutil.rmtree(config.VECTOR_STORE_PATH)
                print("🗑️ Ancien vector store supprimé")
            except:
                pass
        
        os.makedirs(config.VECTOR_STORE_PATH, exist_ok=True)
        
        try:
            # Client simple
            self.client = chromadb.PersistentClient(path=config.VECTOR_STORE_PATH)
            
            # Créer ou récupérer collection
            try:
                self.collection = self.client.get_collection(self.collection_name)
                print(f"✅ Collection existante récupérée ({self.collection.count()} docs)")
            except:
                self.collection = self.client.create_collection(name=self.collection_name)
                print("✅ Nouvelle collection créée")
                
        except Exception as e:
            print(f"❌ Erreur ChromaDB: {e}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Ajoute des documents"""
        if not documents:
            return
        
        ids, texts, metadatas = [], [], []
        
        for i, doc in enumerate(documents):
            doc_id = f"doc_{i}_{hash(doc['source'])}"
            ids.append(doc_id)
            texts.append(doc['text'][:2000])  # Limiter la taille
            metadatas.append({
                'source': doc['source'],
                'chunk_id': str(doc['chunk_id'])
            })
        
        try:
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ {len(documents)} documents ajoutés")
        except Exception as e:
            print(f"⚠️ Erreur ajout documents: {e}")
    
    def search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """Recherche simple"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            formatted = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'score': 0.9  # Score par défaut
                    })
            
            return formatted
            
        except Exception as e:
            print(f"⚠️ Erreur recherche: {e}")
            return []
    
    def get_document_count(self) -> int:
        """Nombre de documents"""
        try:
            return self.collection.count()
        except:
            return 0
    
    def clear(self):
        """Vide la collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(name=self.collection_name)
            print("✅ Collection vidée")
            return True
        except:
            return False