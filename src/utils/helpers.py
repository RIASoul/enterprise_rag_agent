import os
import hashlib
from datetime import datetime
import json
from pathlib import Path

def generate_session_id() -> str:
    """Génère un ID de session unique"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return hashlib.md5(timestamp.encode()).hexdigest()[:12]

def save_conversation_history(session_id: str, messages: list):
    """Sauvegarde l'historique de conversation"""
    try:
        os.makedirs("data/conversations", exist_ok=True)
        
        file_path = Path("data/conversations") / f"{session_id}.json"
        
        data = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'message_count': len(messages),
            'messages': messages
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Erreur sauvegarde historique: {e}")

def load_conversation_history(session_id: str) -> list:
    """Charge l'historique de conversation"""
    try:
        file_path = Path("data/conversations") / f"{session_id}.json"
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('messages', [])
    except:
        pass
    
    return []

def format_file_size(bytes_size: int) -> str:
    """Formate la taille d'un fichier"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def get_supported_file_types() -> list:
    """Retourne les types de fichiers supportés"""
    return ['.pdf', '.txt', '.md', '.docx', '.doc']

def create_data_directories():
    """Crée les répertoires de données nécessaires"""
    directories = [
        "data",
        "data/documents",
        "data/vector_store",
        "data/conversations",
        "static"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Répertoires de données créés")