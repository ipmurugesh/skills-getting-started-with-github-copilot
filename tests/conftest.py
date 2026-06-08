import importlib

import pytest
import src.app as app_module
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    module = importlib.reload(app_module)
    with TestClient(module.app) as client:
        yield client
