from src.provenance.prov import prov_json_for_claims, stable_claim_id

def test_stable_ids():
    a = stable_claim_id("Same claim")
    b = stable_claim_id("Same claim")
    assert a == b
    c = stable_claim_id("Different claim")
    assert a != c

def test_prov_populates_ids():
    claims = [{"text": "The sky is blue"}]
    graph = prov_json_for_claims(claims)
    assert "entity" in graph and len(graph["entity"]) == 1
    assert "id" in claims[0]
