from fastapi.testclient import TestClient
from src.ecl.server.app import app

client = TestClient(app)

def test_verify_smoke():
    r = client.post("/verify", json={"prompt":"Knysna is in the Western Cape?", "models":["stub:gpt"]})
    assert r.status_code == 200
    js = r.json()
    assert "claims" in js and "consensus" in js
    assert len(js["claims"]) >= 1
    assert len(js["consensus"]) >= 1