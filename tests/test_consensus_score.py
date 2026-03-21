from src.consensus.score import score_consensus, score_consensus_legacy


def test_score_consensus_empty():
    score, details = score_consensus([])
    assert score == 0.0
    assert details["pairs"] == 0


def test_score_consensus_with_diversity_adjustment():
    score, details = score_consensus(["a", "a"], router_meta={"diversity_score": 0.8})
    assert 0.0 <= score <= 1.0
    assert details["diversity_score"] == 0.8


def test_score_consensus_legacy_shape():
    out = score_consensus_legacy([{"id": "c1"}], ["m1", "m2"])
    assert out[0]["claim_id"] == "c1"
    assert out[0]["agreement_score"] > 0
