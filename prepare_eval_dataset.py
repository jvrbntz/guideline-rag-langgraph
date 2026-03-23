#!/usr/bin/env python3

"""
Questions dataset pipeline

Parses the 12-question ground truth evaluation set from
data/test_questions.md and writes a structured JSON dataset to data/test_questions.json.

Run once before evaluate.py, or re-run after modifying test_questions.md.

Usage:
    uv run python prepare_eval_dataset.py
"""

import json
import re
from pathlib import Path


def parse_eval_dataset(input_path: str, output_path: str) -> None:
    """Parse markdown questions and write structured JSON to output_path."""
    content = Path(input_path).read_text()
    blocks = content.split("## Q")[1:]
    results = []

    def extract(label, block):
        """Extract a field value from a markdown question block."""
        pattern = rf"\*\*{label}:\*\*\s*(.+?)(?=\*\*|\Z)"
        match = re.search(pattern, block, re.DOTALL)
        return match.group(1).strip().replace("\n\n---", "").strip() if match else ""

    for block in blocks:
        question_id = "Q" + block.split(":")[0].strip()
        results.append(
            {
                "question_id": question_id,
                "question": extract("Question", block),
                "expected_answer": extract("Expected answer", block),
                "evidence_strength": extract("Evidence strength", block),
                "source_location": extract("Source location", block),
                "what_this_tests": extract("What this tests", block),
            }
        )

    Path(output_path).write_text(json.dumps(results, indent=2))
    print(f"Saved {len(results)} records to {output_path}")
    print(results[0])

    return None


if __name__ == "__main__":
    parse_eval_dataset(
        input_path="data/test_questions.md", output_path="data/test_questions.json"
    )
