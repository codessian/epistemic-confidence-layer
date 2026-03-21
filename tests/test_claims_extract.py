from src.claims.extract import heuristic_extract


def test_heuristic_extract_question_single_claim():
    claims = heuristic_extract("Is TLS required?")
    assert len(claims) == 1
    assert claims[0]["text"] == "Is TLS required?"
    assert claims[0]["id"].startswith("c_")


def test_heuristic_extract_sentence_split():
    claims = heuristic_extract("One. Two. Three.")
    assert [claim["text"] for claim in claims] == ["One", "Two", "Three"]


def test_heuristic_extract_empty_input_returns_empty():
    assert heuristic_extract("   ") == []


def test_heuristic_extract_is_deterministic_for_same_text():
    first = heuristic_extract("Same text.")
    second = heuristic_extract("Same text.")
    assert first[0]["id"] == second[0]["id"]
    assert first[0]["hash"] == second[0]["hash"]
