from app import app

def test_home_page():
    client = app.test_client()
    res = client.get("/")
    # Just check app runs and returns 200
    assert res.status_code == 200
    # At least the site header text should appear
    assert b"DevOps News Aggregator" in res.data