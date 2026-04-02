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
# V1: CHUNK_SIZE=512, CHUNK_OVERLAP=50 — caused mid-sentence splits on multi-part recommendations (Q5, Q6)
# V2: increased to reduce boundary splits
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200

# Eval output
EVAL_OUTPUT_PATH = "data/eval_results_v2_chunk1024.json"

# Retrieval
RETRIEVAL_K = 5

# Vector Store
COLLECTION_NAME = "cap_guideline"

# Embedding model
OLLAMA_EMBED_MODEL = "nomic-embed-text"

# LLM
OLLAMA_MODEL = "llama3.1:8b"

# Page index where non-clinical content begins (0-indexed).
# For the ATS/IDSA 2019 CAP guideline, pages 16-22 are references
# and committee disclosures. Document-specific — update if swapping PDFs.
PDF_CONTENT_PAGES = 16

# Answer relevance thresholds
ANSWER_RELEVANCE_GOOD = 0.75
ANSWER_RELEVANCE_ACCEPTABLE = 0.50
