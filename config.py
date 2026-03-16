"""
Configuration settings.

All tunable parameters, file paths, and model settings.
"""

from pathlib import Path


# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_PATH = BASE_DIR / "vector_store" / "chroma_db"

# Source document
PDF_FILENAME = "metlay-et-al-2019-diagnosis-and-treatment-of-adults-with-community-acquired-pneumonia-an-official-clinical-practice.pdf"

# Chunking
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# Retrieval
RETRIEVAL_K = 5

# Vector Store
COLLECTION_NAME = "cap_guideline"

# Embedding model
OLLAMA_EMBED_MODEL = "nomic-embed-text"

# LLM
OLLAMA_MODEL = "llama3.1:8b"
