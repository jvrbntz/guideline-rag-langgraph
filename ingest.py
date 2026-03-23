#!/usr/bin/env python3

"""
Ingestion pipeline

Loads the ATS/IDSA 2019 CAP guidelines PDF, splits it into chunks,
generates embeddings, and persists to a local ChromaDB vector store.

Usage:
    uv run python ingest.py
"""

import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config

load_dotenv()


def load_pdf(pdf_path: Path) -> list:
    """Load PDF and return list of LangChain Documents, one per page."""
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    documents = documents[: config.PDF_CONTENT_PAGES]
    for doc in documents:
        doc.metadata["source"] = Path(doc.metadata["source"]).name
    print(f"Loaded {len(documents)} pages from {pdf_path.name}")
    return documents


def chunk_documents(documents: list) -> list:
    """Split documents into chunks using recursive character splitting."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} pages")
    return chunks


def build_vector_store(chunks: list) -> Chroma:
    """Embed chunks and persist to ChromaDB.

    Wipes any existing collection before ingesting to prevent duplicates.
    """
    if config.CHROMA_DB_PATH.exists():
        shutil.rmtree(config.CHROMA_DB_PATH)
    config.CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

    embeddings = OllamaEmbeddings(model=config.OLLAMA_EMBED_MODEL)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.CHROMA_DB_PATH),
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB at {config.CHROMA_DB_PATH}")
    return vector_store


def main():
    """Orchestrate the ingestion pipeline"""
    pdf_path = config.DATA_DIR / config.PDF_FILENAME

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    documents = load_pdf(pdf_path)
    chunks = chunk_documents(documents)
    build_vector_store(chunks)

    print("\nIngestion complete.")
    print(f" Pages loaded: {len(documents)}")
    print(f" Chunks created: {len(chunks)}")
    print(f" Vector store: {config.CHROMA_DB_PATH}")


if __name__ == "__main__":
    main()
