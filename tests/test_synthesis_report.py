from src.synthesis.report import markdown_summary


def test_markdown_summary_with_consensus():
    claims = [{"id": "c1", "text": "Claim A", "hash": "abc"}]
    consensus = [{"claim_id": "c1", "ecs": 0.8, "agreement_score": 0.9, "diversity_score": 0.7}]
    output = markdown_summary(claims, consensus)
    assert "# ECL Report" in output
    assert "Claim A" in output
    assert "ECS: 0.80" in output


def test_markdown_summary_skips_empty_claim_text():
    claims = [{"id": "c1", "text": "   ", "hash": "x"}]
    output = markdown_summary(claims, [])
    assert "Claim" not in output


def test_markdown_summary_handles_missing_consensus_fields():
    claims = [{"id": "c1", "text": "Claim", "hash": "x"}]
    consensus = [{"claim_id": "c1"}]
    output = markdown_summary(claims, consensus)
    assert "ECS: 0.00" in output
