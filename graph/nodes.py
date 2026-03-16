"""
Node functions for the GuidelineGraph pipeline.

Each node reads from and writes to the shared GraphState object.
Nodes: retrieve, grade_documents, generate
"""

from typing import Literal

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

import config
from graph.state import GraphState


class RelevanceGrade(BaseModel):
    """Relevance grade for a retrieved CAP guideline chunk."""

    relevant: Literal["yes", "no"] = Field(
        description="Is this chunk relevant to the clinical query?"
    )
    reasoning: str = Field(description="Concise explanation of relevance decision.")


_vector_store = None
_grading_chain = None
_generation_chain = None


def _get_vector_store() -> Chroma:
    global _vector_store
    if _vector_store is None:
        embeddings = OllamaEmbeddings(model=config.OLLAMA_EMBED_MODEL)
        _vector_store = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(config.CHROMA_DB_PATH),
        )
    return _vector_store


def _get_grading_chain():
    global _grading_chain
    if _grading_chain is None:
        llm = ChatOllama(model=config.OLLAMA_MODEL, temperature=0)
        _grading_chain = grading_prompt | llm.with_structured_output(RelevanceGrade)
    return _grading_chain


def _get_generation_chain():
    global _generation_chain
    if _generation_chain is None:
        llm = ChatOllama(model=config.OLLAMA_MODEL, temperature=0)
        _generation_chain = generation_prompt | llm
    return _generation_chain


grading_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert in evaluating retrieved document for relevance to a user clinical query.
    
    Query: {query}
    Document: {document}
    
    Instructions:
    - Mark 'yes' if the document is helpful in answering the clinical query.
    - Mark 'no' if the document is unrelated or unhelpful.
    - Provide a concise and clear reasoning behind your decision.
    
    Be strict - only mark 'yes' if the document is genuinely useful.
    """
)


generation_prompt = ChatPromptTemplate.from_template(
    """
    You are a clinical reference assistant helping clinicians query the 
    ATS/IDSA 2019 Community-Acquired Pneumonia (CAP) guideline.

    Use only the provided guideline excerpts to answer the query.
    If the excerpts do not contain enough information, say so clearly.
    Always note the evidence strength (Strong/Conditional) where present.
    Do not recommend treatment for real patients.

    Guideline excerpts:
    {context}

    Query: {query}

    Answer:
    """
)


def retrieve(state: GraphState) -> dict:
    """
    Retrieve relevant chunks from ChromaDB based on the query.

    Reads:  state["query"]
    Writes: state["documents"]
    """
    query = state["query"]
    retrieved_docs = _get_vector_store().similarity_search(query, k=config.RETRIEVAL_K)

    return {"documents": retrieved_docs}


def grade_documents(state: GraphState) -> dict:
    """
    Grade retrieved documents for relevance to the query.

    Reads:  state["query"], state["documents"]
    Writes: state["filtered_documents"]
    """
    query = state["query"]
    documents = state["documents"]

    filtered_documents = []

    for doc in documents:
        grade = _get_grading_chain().invoke({"query": query, "document": doc.page_content})
        if grade.relevant == "yes":
            filtered_documents.append(doc)

    print(f"Kept {len(filtered_documents)}/{len(documents)} documents after grading.")
    return {"filtered_documents": filtered_documents}


def generate(state: GraphState) -> dict:
    """Generate a referenced answer from filtered guideline chunks.

    Reads:  state["query"], state["filtered_documents"]
    Writes: state["answer"]
    """
    query = state["query"]
    filtered_docs = state["filtered_documents"]

    if filtered_docs:
        context_parts = []
        for doc in filtered_docs:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "unknown")
            context_parts.append(f"[Page {page} | {source}]\n{doc.page_content}")
        context_text = "\n\n".join(context_parts)
    else:
        context_text = "No relevant guideline excerpts found for this query."

    response = _get_generation_chain().invoke({"query": query, "context": context_text})

    return {"answer": response.content}
