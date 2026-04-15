#!/usr/bin/env python3

"""
Evaluation pipeline

Runs 12 ground truth questions from data/test_questions.json through
the RAG pipeline and scores each response against three metrics:
Faithfulness, Answer Relevance, and Citation Present.

Results are saved to data/eval_results.json.

Usage:
    uv run python evaluate.py
"""

import json
import logging
from pathlib import Path

from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer, util

from config import (
    ANSWER_RELEVANCE_ACCEPTABLE,
    ANSWER_RELEVANCE_GOOD,
    EVAL_OUTPUT_PATH,
    LOG_LEVEL,
    OLLAMA_MODEL,
    PDF_FILENAME,
)
from logger import get_logger
from query import run_query

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)

logger = get_logger(__name__)

FAITHFULNESS_PROMPT = """
You are evaluating the faithfulness between an LLM-generated answer and a retrieved context.
Score how faithful the answer is to the context on a scale of 1-3.

Score definitions:
1 = answer contradicts the retrieved context, or makes claims entirely absent from it
2 = answer is partially grounded, some claims are supported but others introduce information not in the context
3 = answer is fully grounded in the retrieved context, no claims beyond what the context states

Answer: {answer}
Context: {context}

Return your output as JSON: {{"score": <int>, "reason": "<one sentence>"}}
"""

_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def check_citation(answer: str) -> bool:
    """Check if the generated answer contains a source citation."""
    return PDF_FILENAME in answer


def score_answer_relevance(generated: str, expected: str) -> float:
    """Compute cosine similarity between generated and expected answers."""

    embedding_generated = _embedding_model.encode(generated)
    embedding_expected = _embedding_model.encode(expected)

    return float(util.cos_sim(embedding_generated, embedding_expected))


def grade_answer_relevance(score: float) -> int:
    """Convert cosine similarity score to 1-3 rubric scale."""
    if score >= ANSWER_RELEVANCE_GOOD:
        return 3
    elif score >= ANSWER_RELEVANCE_ACCEPTABLE:
        return 2
    else:
        return 1


def score_faithfulness(answer: str, context: str) -> int:
    """Score faithfulness of generated answer against retrieved context using LLM judge."""
    llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)
    prompt = FAITHFULNESS_PROMPT.format(answer=answer, context=context)
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
        return int(result["score"])
    except (json.JSONDecodeError, KeyError):
        logger.warning(
            f"score_faithfulness: could not parse score. Raw response: {response.content}"
        )
        return 0


def run_evaluation(dataset_path: str, output_path: str) -> list:
    """Evaluate test questions from a dataset and stores the results in a json file."""
    eval_results = []
    test_questions = json.loads(Path(dataset_path).read_text())
    for record in test_questions:
        logger.info(f"run_evaluation: evaluating {record['question_id']}...")
        result = run_query(record["question"])
        answer = result["answer"]
        context = "\n\n".join(
            [doc.page_content for doc in result["filtered_documents"]]
        )
        answer_relevance_score = score_answer_relevance(
            answer, record["expected_answer"]
        )
        eval_results.append(
            {
                "question_id": record["question_id"],
                "faithfulness": score_faithfulness(answer, context),
                "answer_relevance_score": answer_relevance_score,
                "answer_relevance_grade": grade_answer_relevance(
                    answer_relevance_score
                ),
                "citation_present": check_citation(answer),
            }
        )

    Path(output_path).write_text(json.dumps(eval_results, indent=2))
    return eval_results


def main():
    """Orchestrate the evaluation pipeline."""
    questions_dataset_path = "data/test_questions.json"
    eval_output_path = EVAL_OUTPUT_PATH
    eval_results = run_evaluation(questions_dataset_path, eval_output_path)

    print(f"\nEvaluation complete — {len(eval_results)} questions evaluated.")
    print(f"Results saved to {eval_output_path}")

    # Answer relevance
    score_list = [result["answer_relevance_score"] for result in eval_results]
    avg_ans_rel = sum(score_list) / len(score_list)
    min_ans_rel = min(score_list)
    max_ans_rel = max(score_list)

    grade_list = [result["answer_relevance_grade"] for result in eval_results]
    grade_1 = grade_list.count(1)
    grade_2 = grade_list.count(2)
    grade_3 = grade_list.count(3)

    # Faithfulness
    faith_list = [result["faithfulness"] for result in eval_results]
    faith_1 = faith_list.count(1)
    faith_2 = faith_list.count(2)
    faith_3 = faith_list.count(3)

    # Citation present
    citation_list = [result["citation_present"] for result in eval_results]
    citation_count = citation_list.count(True)

    # Print summary
    print(f"\nFaithfulness:      1={faith_1}  2={faith_2}  3={faith_3}")
    print(f"Answer Relevance:  1={grade_1}  2={grade_2}  3={grade_3}")
    print(
        f"Answer Relevance:  min={min_ans_rel:.2f}  max={max_ans_rel:.2f}  avg={avg_ans_rel:.2f}"
    )
    print(f"Citation Present:  {citation_count}/{len(eval_results)}")


if __name__ == "__main__":
    main()
