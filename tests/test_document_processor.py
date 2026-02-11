import pytest
import tempfile
import os
from src.core.document_processor import DocumentProcessor

def test_document_processor_initialization():
    """Test l'initialisation du processeur de documents"""
    processor = DocumentProcessor()
    assert processor is not None
    assert hasattr(processor, 'chunk_size')
    assert hasattr(processor, 'chunk_overlap')

def test_text_chunking():
    """Test le découpage de texte"""
    processor = DocumentProcessor()
    
    # Créer un texte de test
    test_text = "Ceci est un test. " * 100  # Environ 2000 caractères
    
    chunks = processor._chunk_text(test_text)
    
    assert len(chunks) > 0
    for chunk in chunks:
        assert len(chunk) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])