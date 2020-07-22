from test_fixture import app

def test_app_creates(app):
    assert app,'app creation failed'
