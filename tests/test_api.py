from fastapi.testclient import TestClient

from src.server.app import app

client = TestClient(app)


def test_verify_response_schema_includes_request_id_route_id_errors():
    r = client.post("/verify", json={"prompt": "Knysna is in the Western Cape?", "contains_pii": False})
    assert r.status_code == 200
    js = r.json()
    assert js["x_schema_version"] == "1.2"
    assert "request_id" in js
    assert "route_id" in js
    assert "errors" in js and isinstance(js["errors"], list)
    assert "claims" in js and isinstance(js["claims"], list)
    assert "consensus" in js and "score" in js["consensus"]


def test_health_alias_exists_while_livez_readyz_are_primary():
    assert client.get("/health").status_code == 200
    assert client.get("/livez").status_code == 200
    assert client.get("/readyz").status_code in {200, 503}


def test_verify_422_on_invalid_payload():
    r = client.post("/verify", json={"prompt": "", "contains_pii": False})
    assert r.status_code == 422
