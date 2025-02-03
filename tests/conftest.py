from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry

@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
  
  def fake_time_hook(mapper, connection, target):
    if hasattr(target, 'created_at'):
      target.created_at = time
  
  event.listen(model, 'before_insert', fake_time_hook)

  yield time

  event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
  return _mock_db_time


# Ao criar fixture o nome da função da fixture pode ser passada como parametro no teste o pytest vai usar a fixture
@pytest.fixture
def client():
  return TestClient(app)


@pytest.fixture
def session():
  engine = create_engine('sqlite:///:memory:')
  table_registry.metadata.create_all(engine)

  '''
  with É comumente usado para trabalhar com arquivos, conexões de banco de dados, sockets ou qualquer recurso que precise ser aberto e fechado corretamente.
  Substitui o uso de try/finally: Simplifica o código, evitando a necessidade de escrever blocos try/finally para garantir que os recursos sejam liberados.

   A palavra-chave yield é usada em funções para criar geradores. Um gerador é um tipo especial de iterador que produz valores sob demanda, em vez de calcular todos os valores de uma vez.

    Para que serve?
    Iteração eficiente: Permite gerar valores um de cada vez, economizando memória.

    Pausa e retomada: A função pode ser pausada no yield e retomada posteriormente, mantendo seu estado.

    Uso em fixtures: No pytest, yield é usado em fixtures para separar o código de setup (configuração) do teardown (limpeza).
  '''
  with Session(engine) as session:
    yield session

  table_registry.metadata.drop_all(engine)
