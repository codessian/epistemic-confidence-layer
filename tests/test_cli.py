import json
import sys

import src.cli as cli


def test_cli_success(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ecl", "hello", "--host", "http://localhost:8000"])

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": True}

    def fake_post(url, json, headers, timeout):
        assert url.endswith("/verify")
        assert json["prompt"] == "hello"
        return FakeResponse()

    monkeypatch.setattr(cli.requests, "post", fake_post)
    rc = cli.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert json.loads(out)["ok"] is True


def test_cli_failure(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ecl", "hello"])

    def fake_post(url, json, headers, timeout):
        raise cli.requests.RequestException("boom")

    monkeypatch.setattr(cli.requests, "post", fake_post)
    rc = cli.main()
    err = capsys.readouterr().err
    assert rc == 1
    assert "boom" in err
