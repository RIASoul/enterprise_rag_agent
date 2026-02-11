#!/usr/bin/env python3
"""
Application principale - Agent Conversationnel d'Entreprise avec RAG (OpenAI)
"""

# ======================================================
# 🔧 CORRECTION PROBLÈME huggingface_hub (CONSERVÉE)
# ======================================================
import sys
import importlib

modules_a_supprimer = []
for nom_module in list(sys.modules.keys()):
    if "huggingface" in nom_module.lower():
        modules_a_supprimer.append(nom_module)

for nom_module in modules_a_supprimer:
    del sys.modules[nom_module]

try:
    import huggingface_hub
    print(f"✅ huggingface_hub version : {huggingface_hub.__version__}")

    if hasattr(huggingface_hub, "split_torch_state_dict_into_shards"):
        print("✅ Fonction split_torch_state_dict_into_shards disponible")
    else:
        print("⚠️ Fonction split_torch_state_dict_into_shards absente")

except Exception as e:
    print(f"❌ Erreur huggingface_hub : {e}")

# ======================================================
# 🔧 PATHS PYTHON
# ======================================================
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")

sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)

# ======================================================
# 🚀 STREAMLIT
# ======================================================
import streamlit as st


def main():
    """Point d'entrée de l'application"""

    try:
        # Import de l'interface principale
        from src.chat_interface import ChatInterface

    except ImportError as e:
        st.error(f"❌ Erreur d'importation : {e}")
        st.info("Vérifiez la structure du projet.")

        st.code("""
Structure attendue :

enterprise_rag_agent/
├── main.py
├── src/
│   ├── chat_interface.py
│   ├── core/
│   │   ├── document_processor.py
│   │   ├── vector_store.py
│   │   └── retrieval.py
│   ├── models/
│   │   ├── openai.py
│   │   └── fallback_model.py
│   └── utils/
│       └── helpers.py
├── config/
│   └── config.py
└── data/
        """)
        return

    # ==================================================
    # 🧠 LANCEMENT DE L'APPLICATION
    # ==================================================
    try:
        # 🔹 OPTION 1 — Mode fallback (sans OpenAI)
        # app = ChatInterface(force_fallback=True)

        # 🔹 OPTION 2 — Mode OpenAI (RECOMMANDÉ)
        app = ChatInterface(force_fallback=False)

        app.run()

    except Exception as e:
        st.error("❌ Erreur lors du démarrage de l'application")
        st.exception(e)
        st.info("Vérifiez votre clé OpenAI et votre fichier .env")


if __name__ == "__main__":
    main()
