from unittest.mock import Mock, patch
from app import app

def test_home_page_no_api_key(monkeypatch):
    monkeypatch.delenv("NEWSAPI_KEY", raising=False)
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert b"DevOps News Aggregator" in res.data

def test_home_page_with_articles(monkeypatch):
    fake_json = {"articles":[{"title":"Test Article","url":"http://example.com","description":"desc","source":{"name":"Source"}}]}
    fake_resp = Mock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = fake_json
    with patch("app.requests.get", return_value=fake_resp):
        client = app.test_client()
        res = client.get("/")
        assert res.status_code == 200
        assert b"Test Article" in res.data
