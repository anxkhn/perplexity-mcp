"""Tests for SSE payload parsing with console-style output."""

import json

from perplexity.client import parse_sse_message


def test_parse_sse_message_reads_answer_from_final_step() -> None:
    print("console.log -> parsing an answer from the FINAL text step")
    payload = {
        "status": "COMPLETED",
        "text": json.dumps(
            [
                {"step_type": "INITIAL_QUERY", "content": {"query": "hi"}},
                {
                    "step_type": "FINAL",
                    "content": {"answer": json.dumps({"answer": "42", "chunks": ["42"]})},
                },
            ]
        ),
    }

    parsed = parse_sse_message(payload)

    assert parsed["answer"] == "42"
    assert parsed["chunks"] == ["42"]
    assert isinstance(parsed["text"], list)


def test_parse_sse_message_falls_back_to_blocks() -> None:
    print("console.log -> parsing an answer from blocks when text is missing")
    payload = {
        "status": "COMPLETED",
        "text": None,
        "blocks": [
            {
                "intended_usage": "ask_text",
                "markdown_block": {"answer": "block answer", "chunks": ["block ", "answer"]},
            },
            {"intended_usage": "web_results", "web_result_block": {"web_results": []}},
        ],
    }

    parsed = parse_sse_message(payload)

    assert parsed["answer"] == "block answer"
    assert parsed["chunks"] == ["block ", "answer"]


def test_parse_sse_message_tolerates_empty_payload() -> None:
    print("console.log -> parsing a payload with no answer at all")
    assert parse_sse_message({"status": "PENDING"}).get("answer") is None
