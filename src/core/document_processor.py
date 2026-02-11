import os
import tempfile
import re
from pathlib import Path
from typing import List, Dict, Any

from pypdf import PdfReader
from docx import Document
import markdown

from config import config


class DocumentProcessor:
    """
    Processeur de documents multi-format (PDF, TXT, DOCX, MD)
    Optimisé pour un pipeline RAG
    """

    def __init__(self):
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        self.min_paragraph_length = 30

    # =======================
    # Lecture des fichiers
    # =======================

    def _read_pdf(self, file_path: str) -> str:
        """Lit un fichier PDF avec pypdf"""
        text = ""
        try:
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"⚠️ Erreur lecture PDF ({file_path}): {e}")
        return text

    def _read_txt(self, file_path: str) -> str:
        """Lit un fichier TXT"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                return file.read()
        except Exception as e:
            print(f"⚠️ Erreur lecture TXT ({file_path}): {e}")
            return ""

    def _read_docx(self, file_path: str) -> str:
        """Lit un fichier DOCX"""
        try:
            doc = Document(file_path)
            return "\n".join(
                para.text for para in doc.paragraphs if para.text.strip()
            )
        except Exception as e:
            print(f"⚠️ Erreur lecture DOCX ({file_path}): {e}")
            return ""

    def _read_md(self, file_path: str) -> str:
        """Lit un fichier Markdown"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                md_content = file.read()
                html = markdown.markdown(md_content)
                text = re.sub(r"<[^>]+>", "", html)
                return text
        except Exception as e:
            print(f"⚠️ Erreur lecture MD ({file_path}): {e}")
            return ""

    # =======================
    # Extraction texte
    # =======================

    def _extract_text(self, file_path: str) -> str:
        """Extrait le texte selon le type de fichier"""
        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            return self._read_pdf(file_path)
        elif ext == ".txt":
            return self._read_txt(file_path)
        elif ext == ".md":
            return self._read_md(file_path)
        elif ext in [".docx", ".doc"]:
            return self._read_docx(file_path)
        else:
            print(f"⚠️ Format non supporté: {ext}")
            return ""

    # =======================
    # Chunking
    # =======================

    def _chunk_text(self, text: str) -> List[str]:
        """Découpe le texte en chunks avec chevauchement"""
        if not text:
            return []

        text = re.sub(r"\r\n|\r", "\n", text)

        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if len(p.strip()) >= self.min_paragraph_length
        ]

        chunks = []
        current_chunk = []
        current_length = 0

        for para in paragraphs:
            para_length = len(para)

            if current_length + para_length > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))

                if self.chunk_overlap > 0:
                    overlap_words = current_chunk[-self.chunk_overlap // 5 :]
                    current_chunk = overlap_words.copy()
                    current_length = len(" ".join(current_chunk))
                else:
                    current_chunk = []
                    current_length = 0

            current_chunk.append(para)
            current_length += para_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    # =======================
    # Traitement principal
    # =======================

    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Traite un document local"""
        text = self._extract_text(file_path)

        if not text.strip():
            return []

        chunks = self._chunk_text(text)
        documents = []

        for i, chunk in enumerate(chunks, start=1):
            documents.append({
                "text": chunk,
                "source": Path(file_path).name,
                "chunk_id": i,
                "file_path": file_path
            })

        print(f"📄 {Path(file_path).name}: {len(chunks)} chunks créés")
        return documents

    def process_uploaded_file(self, uploaded_file) -> List[Dict[str, Any]]:
        """Traite un fichier uploadé via Streamlit"""
        print(f"⬆️ Traitement fichier uploadé : {uploaded_file.name}")

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(uploaded_file.name).suffix
        ) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        try:
            documents = self.process_document(tmp_path)

            # Conserver le nom original
            for doc in documents:
                doc["source"] = uploaded_file.name

            print(f"✅ {uploaded_file.name}: {len(documents)} chunks traités")
            return documents

        except Exception as e:
            print(f"❌ Erreur traitement {uploaded_file.name}: {e}")
            return []

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Traite tous les documents d'un dossier"""
        directory = Path(directory_path)
        all_documents = []

        if not directory.exists():
            print(f"❌ Dossier introuvable: {directory_path}")
            return []

        supported_ext = {".pdf", ".txt", ".md", ".docx", ".doc"}

        for file_path in directory.iterdir():
            if file_path.suffix.lower() in supported_ext:
                all_documents.extend(
                    self.process_document(str(file_path))
                )

        print(f"📁 Total chunks extraits: {len(all_documents)}")
        return all_documents
