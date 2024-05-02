from fastapi.testclient import TestClient
import unittest
import logging

from backend.main import app
from backend.utils.robust_jsonify import robust_jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestMain(unittest.TestCase):

    def setUp(self) -> None:
       self.client = TestClient(app)

    def test_get_models(self):
        response = self.client.get("/models")
        logger.info(f"response: {response}")

    def test_read_main(self):
        response = self.client.post(
            "/chat/123",
            json={"question": "Who are you?"},
        )
        logger.info(f"response: {response}")
        assert response.status_code == 200
        assert response.json() == {"question": "Hello World"}

