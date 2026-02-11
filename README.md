# 🤖 Agent RAG d'Entreprise

Un agent conversationnel intelligent utilisant la technique RAG (Retrieval-Augmented Generation) pour répondre aux questions à partir de vos documents d'entreprise.

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Formats de documents supportés](#-formats-de-documents-supportés)
- [Modèles LLM disponibles](#-modèles-llm-disponibles)
- [Dépannage](#-dépannage)
- [Contributeurs](#-contributeurs)

## 🎯 Présentation

L'Agent RAG d'Entreprise est une application Streamlit qui permet d'interroger intelligemment vos documents professionnels. Grâce à la technologie RAG, l'application :

1. **Indexe vos documents** dans une base de données vectorielle (ChromaDB)
2. **Recherche** les passages pertinents selon votre question
3. **Génère une réponse** contextuelle via un modèle de langage (Gemini, OpenAI, ou Ollama)

Cette approche garantit des réponses **factuelles** et **traçables**, basées uniquement sur vos documents.

## ✨ Fonctionnalités

- 🔍 **Recherche sémantique** : Trouve les informations pertinentes même avec des formulations différentes
- 📁 **Multi-formats** : Supporte PDF, DOCX, TXT, Markdown
- 💬 **Interface conversationnelle** : Chat intuitif via Streamlit
- 🧠 **Plusieurs modèles LLM** :
  - Google Gemini (recommandé)
  - OpenAI (GPT-4o-mini)
  - Ollama (modèles locaux)
  - Mode fallback (sans API)
- 📊 **Gestion des documents** :
  - Upload de fichiers individuels
  - Chargement de dossiers complets
  - Visualisation du nombre de documents indexés
- 💾 **Historique des conversations** : Sauvegarde automatique de vos échanges
- 🎨 **Interface utilisateur moderne** : Design épuré avec Streamlit

## 🛠️ Technologies utilisées

### Backend
- **Python 3.8+**
- **ChromaDB** : Base de données vectorielle
- **Sentence Transformers** : Embeddings sémantiques (all-MiniLM-L6-v2)
- **LangChain** : Framework RAG (optionnel)

### Modèles LLM
- **Google Gemini API** : Modèle de langage principal
- **OpenAI API** : Alternative GPT-4o-mini
- **Ollama** : Modèles locaux (Llama, etc.)

### Frontend
- **Streamlit** : Interface web interactive

### Traitement de documents
- **pypdf** : Lecture de fichiers PDF
- **python-docx** : Traitement de fichiers Word
- **markdown** : Conversion de fichiers Markdown

## 📦 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Une clé API Google Gemini (recommandé) ou OpenAI
- (Optionnel) Ollama installé pour les modèles locaux

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/RIASoul/enterprise_rag_agent.git
cd enterprise_rag_agent
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Créer le fichier `.env`

Copiez le fichier d'exemple et remplissez vos clés API :

```bash
cp .env.example .env
```

### 2. Configuration des variables d'environnement

Éditez le fichier `.env` :

```env
# ========================================
# Configuration Gemini (RECOMMANDÉ)
# ========================================
GEMINI_API_KEY=votre_cle_api_gemini_ici
MODEL_NAME=gemini-2.0-flash

# ========================================
# Configuration OpenAI (ALTERNATIVE)
# ========================================
OPENAI_API_KEY=votre_cle_api_openai_ici
# MODEL_NAME=gpt-4o-mini

# ========================================
# Configuration Ollama (LOCAL)
# ========================================
OLLAMA_MODEL=llama3:8b
OLLAMA_BASE_URL=http://localhost:11434

# ========================================
# Configuration des embeddings
# ========================================
EMBEDDING_MODEL=all-MiniLM-L6-v2

# ========================================
# Chemins de stockage
# ========================================
VECTOR_STORE_PATH=data/vector_store/chroma_db
DOCUMENTS_PATH=data/documents

# ========================================
# Paramètres du modèle
# ========================================
TEMPERATURE=0.1
MAX_TOKENS=2048

# ========================================
# Configuration RAG
# ========================================
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=4
```

### 3. Obtenir une clé API

#### Google Gemini (Recommandé)
1. Accédez à [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créez une clé API
3. Copiez-la dans votre fichier `.env`

#### OpenAI (Alternative)
1. Accédez à [OpenAI Platform](https://platform.openai.com/api-keys)
2. Créez une clé API
3. Copiez-la dans votre fichier `.env`

#### Ollama (Local)
1. Installez Ollama : [https://ollama.ai](https://ollama.ai)
2. Téléchargez un modèle : `ollama pull llama3:8b`
3. Lancez le serveur : `ollama serve`

## 🎮 Utilisation

### Lancer l'application

```bash
streamlit run main.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Guide d'utilisation

#### 1. Charger des documents

**Option A : Upload de fichiers**
- Cliquez sur "📁 Télécharger des documents" dans la sidebar
- Sélectionnez un ou plusieurs fichiers (PDF, DOCX, TXT, MD)
- Cliquez sur "Charger les documents"

**Option B : Charger un dossier complet**
- Placez vos documents dans le dossier `data/documents/`
- Cliquez sur "📂 Charger dossier automatiquement" dans la sidebar

#### 2. Vérifier l'indexation

- Le nombre de documents indexés s'affiche dans la sidebar
- Un indicateur de taille du vector store est également disponible

#### 3. Poser des questions

- Tapez votre question dans le chat
- L'agent recherchera les passages pertinents
- Il générera une réponse basée uniquement sur vos documents

#### 4. Réinitialiser le système

- Cliquez sur "🔄 Réinitialiser le système RAG" pour :
  - Vider le vector store
  - Supprimer l'historique des conversations
  - Repartir à zéro

### Exemples de questions

```
"Quelles sont les procédures de sécurité décrites dans les documents ?"
"Résume-moi le contrat client ABC"
"Quels sont les délais de livraison mentionnés ?"
"Comment fonctionne le processus d'onboarding ?"
```

## 📂 Structure du projet

```
enterprise_rag_agent/
├── main.py                          # Point d'entrée de l'application
├── requirements.txt                 # Dépendances Python
├── .env.example                     # Template de configuration
├── .env                             # Configuration (à créer)
│
├── config/                          # Configuration de l'application
│   ├── __init__.py
│   ├── config.py                    # Paramètres globaux
│   └── settings.py                  # Paramètres additionnels
│
├── src/                             # Code source principal
│   ├── __init__.py
│   ├── chat_interface.py            # Interface Streamlit
│   │
│   ├── core/                        # Logique métier RAG
│   │   ├── __init__.py
│   │   ├── document_processor.py   # Traitement des documents
│   │   ├── vector_store.py         # Gestion ChromaDB
│   │   └── retrieval.py            # Récupération des documents
│   │
│   ├── models/                      # Wrappers des modèles LLM
│   │   ├── __init__.py
│   │   ├── gemini_model.py         # Google Gemini
│   │   ├── openai.py               # OpenAI GPT
│   │   ├── ollama_model.py         # Ollama (local)
│   │   └── fallback_model.py       # Mode sans API
│   │
│   └── utils/                       # Utilitaires
│       ├── __init__.py
│       └── helpers.py               # Fonctions auxiliaires
│
├── data/                            # Données de l'application
│   ├── documents/                   # Documents à indexer
│   ├── vector_store/                # Base vectorielle ChromaDB
│   └── conversations/               # Historique des chats
│
└── tests/                           # Tests unitaires
    ├── test_document_processor.py
    └── test_simple.py
```

## 📄 Formats de documents supportés

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Documents Adobe PDF |
| Word | `.docx` | Microsoft Word (format moderne) |
| Texte | `.txt` | Fichiers texte brut |
| Markdown | `.md` | Documents Markdown |

### Limitations

- **Taille maximale** : Recommandé < 50 MB par fichier
- **Images** : Le texte dans les images n'est pas extrait (pas d'OCR)
- **Tableaux** : Extraction basique, mise en forme peut être perdue
- **Ancien format Word** : Les fichiers `.doc` ne sont pas supportés (convertir en `.docx`)

## 🧠 Modèles LLM disponibles

### 1. Google Gemini (Recommandé)

**Avantages** :
- ✅ Rapide et performant
- ✅ Gratuit (avec quota généreux)
- ✅ Support multilingue excellent
- ✅ Contexte étendu (varie selon le modèle)

**Configuration** :
```python
# Dans main.py
app = ChatInterface(force_fallback=False)  # Mode Gemini
```

### 2. OpenAI GPT-4o-mini

**Avantages** :
- ✅ Très précis
- ✅ Excellent raisonnement
- ⚠️ Payant (facturation à l'usage)

**Configuration** :
Modifier `src/chat_interface.py` pour utiliser le modèle OpenAI

### 3. Ollama (Local)

**Avantages** :
- ✅ 100% gratuit
- ✅ Aucune donnée envoyée sur Internet
- ✅ Pas de limite de requêtes
- ⚠️ Nécessite une bonne configuration matérielle

**Configuration** :
1. Installer Ollama
2. Télécharger un modèle : `ollama pull llama3:8b`
3. Modifier le code pour utiliser `OllamaModel`

### 4. Mode Fallback (Sans API)

**Avantages** :
- ✅ Fonctionne sans clé API
- ⚠️ Réponses basiques (pas de génération intelligente)

**Configuration** :
```python
# Dans main.py
app = ChatInterface(force_fallback=True)  # Mode fallback
```

## 🔧 Dépannage

### Problème : "GEMINI_API_KEY non configurée"

**Solution** :
1. Vérifiez que le fichier `.env` existe à la racine du projet
2. Assurez-vous que la clé API est correctement copiée
3. Redémarrez l'application

### Problème : "Erreur ChromaDB"

**Solution** :
```bash
# Supprimer le vector store corrompu
rm -rf data/vector_store/chroma_db

# Relancer l'application
streamlit run main.py
```

### Problème : "Module 'huggingface_hub' introuvable"

**Solution** :
```bash
# Réinstaller les dépendances
pip install --upgrade huggingface-hub transformers sentence-transformers
```

### Problème : "Aucun document trouvé"

**Causes possibles** :
- Les documents ne sont pas dans le bon dossier (`data/documents/`)
- Le vector store n'a pas été initialisé
- Les fichiers ne sont pas dans un format supporté

**Solution** :
1. Vérifiez l'emplacement des fichiers
2. Cliquez sur "Charger dossier automatiquement"
3. Vérifiez le compteur de documents dans la sidebar

### Problème : Performance lente

**Optimisations** :
1. Réduire `CHUNK_SIZE` dans `.env` (ex: 500)
2. Réduire `TOP_K_RESULTS` (ex: 3)
3. Utiliser un modèle plus léger (Gemini-flash)
4. Limiter la taille des documents

### Problème : Réponses non pertinentes

**Solutions** :
1. Augmenter `TOP_K_RESULTS` pour récupérer plus de contexte
2. Améliorer la qualité des documents (supprimer le bruit)
3. Reformuler la question de manière plus précise
4. Vérifier que les documents pertinents sont bien indexés

## 📝 Bonnes pratiques

### Préparation des documents

1. **Nettoyage** : Supprimez les pages de couverture, index inutiles
2. **Organisation** : Un document = un sujet
3. **Format** : Préférez PDF ou DOCX pour une meilleure extraction
4. **Nommage** : Utilisez des noms de fichiers descriptifs

### Formulation des questions

1. **Précision** : Posez des questions spécifiques
2. **Contexte** : Mentionnez le sujet ou le document si possible
3. **Mots-clés** : Utilisez le vocabulaire présent dans vos documents
4. **Longueur** : Questions courtes et claires

### Sécurité

1. **Clés API** : Ne jamais commiter le fichier `.env`
2. **Documents sensibles** : Utilisez Ollama pour traiter localement
3. **Accès** : Restreindre l'accès à l'application en production
4. **Sauvegarde** : Sauvegardez régulièrement `data/vector_store/`

## 🤝 Contributeurs

- Développé avec ❤️ pour faciliter l'accès à l'information d'entreprise

## 📄 Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

## 🔗 Liens utiles

- [Documentation Streamlit](https://docs.streamlit.io)
- [Documentation ChromaDB](https://docs.trychroma.com)
- [Documentation Google Gemini](https://ai.google.dev/docs)
- [Documentation Sentence Transformers](https://www.sbert.net)

## 🎓 Ressources supplémentaires

### Qu'est-ce que le RAG ?

Le **RAG (Retrieval-Augmented Generation)** est une technique qui combine :
1. **Retrieval (Récupération)** : Recherche de documents pertinents
2. **Augmentation** : Enrichissement de la requête avec le contexte
3. **Generation** : Création d'une réponse par un LLM

Cette approche permet d'avoir des réponses **factuelles**, **à jour**, et **traçables**.

### Concepts clés

- **Embeddings** : Représentation vectorielle des textes pour la recherche sémantique
- **Vector Store** : Base de données optimisée pour la recherche de similarité
- **Chunking** : Découpage des documents en morceaux pour un traitement optimal
- **Prompt Engineering** : Formulation des instructions pour le modèle LLM

---

**Besoin d'aide ?** Ouvrez une issue sur GitHub ou consultez la documentation des technologies utilisées.
