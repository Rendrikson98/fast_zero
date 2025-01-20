import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


# Ao criar fixture o nome da função da fixture pode ser passada como parametro no teste o pytest vai usar a fixture
@pytest.fixture
def client():
  return TestClient(app)
