from types import SimpleNamespace

from src.provenance.prov import prov_from_generations, prov_json_for, stable_claim_id


def test_stable_claim_id_is_stable():
    assert stable_claim_id("abc") == stable_claim_id("abc")
    assert stable_claim_id("abc") != stable_claim_id("xyz")


def test_prov_json_for_contains_activity_and_agent():
    claims = [{"text": "A"}, {"text": "B"}]
    prov = prov_json_for(claims)
    assert "activity:verify" in prov["activity"]
    assert "agent:ecl" in prov["agent"]
    assert len(prov["wasGeneratedBy"]) == 2


def test_prov_from_generations_builds_entities_and_route():
    generations = [
        SimpleNamespace(metadata={"provider_id": "openai", "model": "gpt", "vendor": "openai", "arch_family": "gpt", "latency_ms": 10, "route_id": "r1"})
    ]
    out = prov_from_generations(generations, route_meta={"route_id": "r1"})
    assert out["entities"][0]["id"] == "openai"
    assert out["route"]["route_id"] == "r1"
