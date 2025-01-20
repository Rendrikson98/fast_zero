from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

# banco de dados fake
database = []

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
  return {'message': 'Hello, World!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_html():
  return """
  <html>
    <body>
      <h1>Hello, World!</h1>
    </body>
  </html>
  """


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
  # .model_dump() é um método de modelos do pydantic que converte o objeto em dicionário. Por exemplo, user.model_dump() faria a conversão em {'username': 'nome do usuário', 'password': 'senha do usuário', 'email': 'email do usuário'}. Os ** querem dizer que o dicionário será desempacotado em parâmetros. Fazendo com que a chamada seja equivalente a UserDB(username='nome do usuário', password='senha do usuário', email='email do usuário', id=len(database) + 1)
  user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

  database.append(user_with_id)

  return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
  return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
  if user_id > len(database) or user_id < 1:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado')

  user_with_id = UserDB(**user.model_dump(), id=user_id)
  database[user_id - 1] = user_with_id

  return user_with_id


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int):
  if user_id > len(database) or user_id < 1:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

  del database[user_id - 1]

  return {'message': 'User deleted'}


@app.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(user_id: int):
  if user_id > len(database) or user_id < 1:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

  return database[user_id - 1]
