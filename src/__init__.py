"""
Package src - Contient les modules principaux de l'application RAG
"""

# Rendre les sous-modules accessibles
from . import core
from . import models
from . import utils
from . import chat_interface

__all__ = ['core', 'models', 'utils', 'chat_interface']