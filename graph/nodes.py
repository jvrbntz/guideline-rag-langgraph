"""
Node functions for the GuidelineGraph pipeline.

Each node reads from and writes to the shared GraphState object.
Nodes: retrieve, grade_documents, generate, classify_query, rewrite_query
"""

from typing import Literal

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from pydantic import BaseModel, Field

import config
from graph.state import GraphState


class RelevanceGrade(BaseModel):
    """Relevance grade for a retrieved CAP guideline chunk."""

    relevant: Literal["yes", "no"] = Field(
        description="Is this chunk relevant to the clinical query?"
    )
    reasoning: str = Field(description="Concise explanation of relevance decision.")


class ScopeGrade(BaseModel):
    """Scope classification for a user query."""

    in_scope: Literal["yes", "no"] = Field(
        description="Is this query within scope of the ATS/IDSA 2019 CAP guideline?"
    )

    reasoning: str = Field(description="Concise explanation of scope decision.")


_vector_store = None
_grading_chain = None
_generation_chain = None
_classification_chain = None
_rewrite_chain = None


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


def _get_classification_chain():
    global _classification_chain
    if _classification_chain is None:
        llm = ChatOllama(model=config.OLLAMA_MODEL, temperature=0)
        _classification_chain = classification_prompt | llm.with_structured_output(
            ScopeGrade
        )
    return _classification_chain


def _get_generation_chain():
    global _generation_chain
    if _generation_chain is None:
        llm = ChatOllama(model=config.OLLAMA_MODEL, temperature=0)
        _generation_chain = generation_prompt | llm
    return _generation_chain


def _get_rewrite_chain():
    global _rewrite_chain
    if _rewrite_chain is None:
        llm = ChatOllama(model=config.OLLAMA_MODEL, temperature=0)
        _rewrite_chain = rewrite_prompt | llm
    return _rewrite_chain


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

    Instructons:
    - Return only the answer, do not add unnecessary commentaries. 

    Guideline excerpts:
    {context}

    Query: {query}

    Answer:
    """
)

classification_prompt = ChatPromptTemplate.from_template(
    """
    You are evaluating whether a clinical query is within the scope of the ATS/IDSA 2019 Community-Acquired Pneumonia guideline for adult patients.

    In scope:
    - Adult patients
    - Antibiotic selection, dosing, duration, administration route
    - Site of care: ICU, outpatient, inpatient
    - Diagnostic testing recommendations

    Out of scope:
    - Pediatric patients
    - Non-CAP respiratory infections
    - Unrelated clinical topics 
    - Hospital-acquired pneumonia
    - Pregnant patients

    Query: {query}

    Instructions:
    - Mark "yes" if the query falls within the scope above.
    - Mark "no" if the query is outside the scope above. 
    - Provide concise and clear reasoning for your decision.
    """
)

rewrite_prompt = ChatPromptTemplate.from_template(
    """
    You are improving a clinical query to retrieve better results from the ATS/IDSA 2019 CAP guideline.
    Rephrase the query to be more specific or use different clinical terminology.
    Do not add new clinical meaning, stay true to the original intent. 

    Instructions: 
    - Return only the rewritten query, no explanation or commentary.

    Query: {query}

    Rewritten query:
    """
)


def retrieve(state: GraphState) -> dict:
    """
    Retrieve relevant chunks from ChromaDB based on the query.

    Reads:  state["query"], state["rewrite_query"]
    Writes: state["documents"]
    """
    query = state["rewritten_query"] or state["query"]
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
        grade = _get_grading_chain().invoke(
            {"query": query, "document": doc.page_content}
        )
        if grade.relevant == "yes":
            filtered_documents.append(doc)

    print(f"Kept {len(filtered_documents)}/{len(documents)} documents after grading.")
    return {"filtered_documents": filtered_documents}


def classify_query(state: GraphState) -> dict:
    """
    Classify whether the query is within scope of the CAP guideline.

    Reads:  state["query"]
    Writes: state["query_scope"]
    """
    query = state["query"]

    result = _get_classification_chain().invoke({"query": query})

    return {"query_scope": result.in_scope}


def rewrite_query(state: GraphState) -> dict:
    """
    Rewrites a more specific and relevant clinical query compared to the user's query.

    Reads: state["query"], state["rewritten_query"], state["rewrite_count"]

    Returns: state["rewritten_query"], state["rewrite_count"]
    """
    query = state["rewritten_query"] or state["query"]
    count = state["rewrite_count"]

    response = _get_rewrite_chain().invoke({"query": query})

    return {"rewritten_query": response.content, "rewrite_count": count + 1}


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

    if filtered_docs:
        sources = []
        for doc in filtered_docs:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "unknown")
            sources.append(f"- {source} | Page {page}")
        sources_text = "\n".join(sources)
        answer_with_sources = f"{response.content}\n\nSources:\n{sources_text}"
    else:
        answer_with_sources = response.content

    return {"answer": answer_with_sources}
