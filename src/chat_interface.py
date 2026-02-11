import streamlit as st
from pathlib import Path

from src.core import DocumentProcessor, VectorStore, RAGRetriever
from src.models import GeminiModel, FallbackModel
from src.utils import (
    generate_session_id,
    save_conversation_history,
    load_conversation_history,
    get_supported_file_types,
    create_data_directories,
)
from config import config


class ChatInterface:
    """Interface Streamlit – RAG + Gemini (Sidebar V2)"""

    def __init__(self, force_fallback: bool = False):
        create_data_directories()

        if "document_processor" not in st.session_state:
            st.session_state.document_processor = DocumentProcessor()
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = VectorStore()
        if "rag_retriever" not in st.session_state:
            st.session_state.rag_retriever = RAGRetriever(st.session_state.vector_store)

        self.document_processor = st.session_state.document_processor
        self.vector_store = st.session_state.vector_store
        self.rag_retriever = st.session_state.rag_retriever

        if "llm_model" not in st.session_state:
            if force_fallback:
                st.session_state.llm_model = FallbackModel()
                st.session_state.model_status = "fallback"
                st.session_state.model_message = "Mode secours (fallback)"
            else:
                try:
                    st.session_state.llm_model = GeminiModel()
                    st.session_state.model_status = "gemini"
                    st.session_state.model_message = "Gemini connecté"
                except Exception as e:
                    st.session_state.llm_model = FallbackModel()
                    st.session_state.model_status = "fallback"
                    st.session_state.model_message = f"Gemini indisponible : {str(e)[:120]}"

        self.llm_model = st.session_state.llm_model
        self._init_session_state()

    def _init_session_state(self):
        if "session_id" not in st.session_state:
            st.session_state.session_id = generate_session_id()

        if "messages" not in st.session_state:
            history = load_conversation_history(st.session_state.session_id)
            st.session_state.messages = history if history else []

        if "documents" not in st.session_state:
            st.session_state.documents = []

        if "document_count" not in st.session_state:
            st.session_state.document_count = self.vector_store.get_document_count()

        if "folder_loaded" not in st.session_state:
            st.session_state.folder_loaded = False

        if "auto_save" not in st.session_state:
            st.session_state.auto_save = True

        if "auto_check_files" not in st.session_state:
            st.session_state.auto_check_files = True

    def setup_page(self):
        st.set_page_config(
            page_title="🤖 Agent RAG d’Entreprise",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    # ---------------- Sidebar V2 ----------------

    def _disk_size_mb(self, folder: str) -> float:
        p = Path(folder)
        if not p.exists():
            return 0.0
        total = 0
        for f in p.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
        return total / (1024 * 1024)

    def initialize_rag_system(self):
        # Reset RAG + conversation (sans casser le design)
        self.vector_store.clear()
        st.session_state.documents = []
        st.session_state.document_count = 0
        st.session_state.folder_loaded = False

        st.session_state.session_id = generate_session_id()
        st.session_state.messages = []
        save_conversation_history(st.session_state.session_id, st.session_state.messages)

        st.success("✅ Système RAG initialisé.")

    def clear_conversation_only(self):
        st.session_state.session_id = generate_session_id()
        st.session_state.messages = []
        save_conversation_history(st.session_state.session_id, st.session_state.messages)
        st.success("✅ Conversation effacée.")

    def render_sidebar(self):
        with st.sidebar:
            st.title("📚 Documents")

            # Badge modèle
            if st.session_state.model_status == "gemini":
                st.success("✨ Gemini (Cloud)")
            else:
                st.warning("🔧 Modèle fallback")

            st.caption(st.session_state.model_message)
            st.divider()

            tab_conf, tab_files, tab_hist = st.tabs(["⚙️ Configuration", "📁 Fichiers", "🕘 Historique"])

            # ---- Configuration ----
            with tab_conf:
                st.subheader("Configuration du Système")

                if st.button("🔄 Initialiser le Système RAG", use_container_width=True):
                    self.initialize_rag_system()

                # Statut RAG
                if st.session_state.document_count > 0:
                    st.success("✅ Système RAG actif")
                else:
                    st.info("ℹ️ Charge des documents pour activer le RAG")

                st.divider()
                st.subheader("Options")
                st.session_state.auto_save = st.checkbox("Sauvegarde automatique", value=st.session_state.auto_save)
                st.session_state.auto_check_files = st.checkbox("Vérification automatique des nouveaux fichiers", value=st.session_state.auto_check_files)

                if st.button("🧹 Effacer la conversation actuelle", use_container_width=True):
                    self.clear_conversation_only()

                st.divider()
                st.subheader("Statistiques")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Documents (chunks)", st.session_state.document_count)
                    st.metric("Fichiers", len({d.get("source") for d in st.session_state.documents}) if st.session_state.documents else 0)
                with col2:
                    st.metric("Modèle", "Gemini" if st.session_state.model_status == "gemini" else "Fallback")
                    st.metric("Taille DB", f"{self._disk_size_mb(config.VECTOR_STORE_PATH):.1f} MB")

                # Debug modèle (si erreur)
                last_err = getattr(self.llm_model, "last_error", None)
                if last_err:
                    with st.expander("🛠️ Debug modèle (erreur Gemini)"):
                        st.code(last_err)

            # ---- Fichiers ----
            with tab_files:
                uploaded_files = st.file_uploader(
                    "Uploader des documents",
                    type=get_supported_file_types(),
                    accept_multiple_files=True,
                )

                if uploaded_files and st.button("🚀 Traiter les fichiers", use_container_width=True):
                    self.process_files(uploaded_files)

                st.divider()

                folder_path = st.text_input("Chemin du dossier", value=config.DOCUMENTS_PATH)
                st.button(
                    "📂 Charger dossier",
                    disabled=st.session_state.folder_loaded,
                    on_click=self.load_folder,
                    args=(folder_path,),
                    use_container_width=True,
                )

                st.divider()
                if st.button("🗑️ Vider la base", use_container_width=True):
                    self.clear_all()

            # ---- Historique ----
            with tab_hist:
                st.caption(f"Session : {st.session_state.session_id[:8]}")
                if st.session_state.messages:
                    st.write("Derniers messages :")
                    for m in st.session_state.messages[-6:]:
                        st.write(f"**{m['role']}**: {m['content'][:120]}")
                else:
                    st.info("Aucun message pour le moment.")

    # ---------------- RAG ops ----------------

    def process_files(self, uploaded_files):
        with st.spinner("Traitement des fichiers..."):
            for file in uploaded_files:
                documents = self.document_processor.process_uploaded_file(file)
                if documents:
                    self.vector_store.add_documents(documents)
                    st.session_state.documents.extend(documents)

            st.session_state.document_count = self.vector_store.get_document_count()
            st.success("✅ Documents indexés avec succès")

    def load_folder(self, folder_path: str):
        folder = Path(folder_path)

        if not folder.exists():
            st.error("❌ Dossier introuvable")
            return

        if st.session_state.folder_loaded:
            st.info("📁 Dossier déjà chargé")
            return

        with st.spinner("Chargement du dossier..."):
            documents = self.document_processor.process_directory(folder)

            if not documents:
                st.warning("⚠️ Aucun document valide trouvé")
                return

            self.vector_store.add_documents(documents)
            st.session_state.documents.extend(documents)
            st.session_state.document_count = self.vector_store.get_document_count()
            st.session_state.folder_loaded = True

            st.success(f"📂 Dossier chargé ({len(documents)} chunks)")

    def clear_all(self):
        self.vector_store.clear()
        st.session_state.documents = []
        st.session_state.document_count = 0
        st.session_state.folder_loaded = False
        st.success("🗑️ Base vidée")

    # ---------------- Chat ----------------

    def render_chat(self):
        st.title("🤖 Agent Conversationnel RAG")

        if st.session_state.document_count == 0:
            st.warning("Veuillez charger des documents avant de poser une question.")
            return

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        question = st.chat_input("Votre question…")
        if question:
            self.handle_question(question)

    def handle_question(self, question: str):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Recherche et génération…"):
                relevant_docs = self.rag_retriever.retrieve(question)
                context = self.rag_retriever.format_context(relevant_docs)

                response = self.llm_model.generate_response(
                    query=question,
                    context=context,
                    conversation_history=st.session_state.messages[:-1],
                )

                st.markdown(response)

                if relevant_docs:
                    with st.expander("📚 Sources"):
                        st.markdown(self.rag_retriever.format_sources_for_display(relevant_docs))

                st.session_state.messages.append({"role": "assistant", "content": response})

                if st.session_state.auto_save:
                    save_conversation_history(st.session_state.session_id, st.session_state.messages)

    def run(self):
        self.setup_page()
        self.render_sidebar()
        self.render_chat()
