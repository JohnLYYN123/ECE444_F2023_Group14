from backend.app import create_app
import pytest


@pytest.fixture
def app():
    app = create_app()
    return app


def test_displayMainPageWithEmptyEvent(app):
    pageInfo = []
    tester = app.test_client()
    response = tester.post("/mainPage", data=dict(pageInfo), content_type="html/text")

    assert response.status_code == 200