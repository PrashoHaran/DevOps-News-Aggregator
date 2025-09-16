from unittest.mock import Mock, patch
from app import app

def test_home_page_no_api_key(monkeypatch):
    # Remove NEWSAPI_KEY from environment to simulate missing key
    monkeypatch.delenv("NEWSAPI_KEY", raising=False)
    client = app.test_client()
    res = client.get("/")
    
    # Page should load successfully
    assert res.status_code == 200
    # It should either show the site header or the fallback "NEWSAPI_KEY missing" message
    assert b"DevOps News Aggregator" in res.data or b"NEWSAPI_KEY missing" in res.data


def test_home_page_with_articles(monkeypatch):
    # Fake NewsAPI response
    fake_json = {
        "articles": [
            {
                "title": "Test Article",
                "url": "http://example.com",
                "description": "desc",
                "source": {"name": "Source"}
            }
        ]
    }
    fake_resp = Mock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = fake_json

    # Patch requests.get inside app.py
    with patch("app.requests.get", return_value=fake_resp):
        client = app.test_client()
        res = client.get("/")
        
        # Page should load successfully
        assert res.status_code == 200
        # It should contain our fake article title
        assert b"Test Article" in res.data
