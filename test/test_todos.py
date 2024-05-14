from fastapi.testclient import TestClient
from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi import status
from TodoApp.routers.auth import get_db,get_current_user
from ..database import Base
from ..main import app
import pytest
from ..models import Todos


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username":"sangam chhetri","id":2,"role":'user'}


app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user


client = TestClient(app)

#  id = Column(Integer, primary_key=True,index=True)
#     title = Column(String)
#     description = Column(String)
#     priority = Column(Integer)
#     complete = Column(Boolean, default = False)
#     owner_id

@pytest.fixture
def test_todo():
    todo = Todos(
        priority= 4,
        owner_id= 2,
        complete= False,
        title= "hair cut",
        description= "get a hair cut"
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("SELECT * FROM TODOS"))
        connection.execute(text("DELETE FROM TODOS WHERE owner_id==1"))
        connection.execute(text("DELETE FROM TODOS"))
        connection.commit()


def test_read_todos(test_todo):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == test_todo.title

# def test_read_all_authenticated(test_todo):
#     response = client.post("/")
#     print("Response status code:", response.status_code)  # Debugging output
#     print("Response JSON:", response)  
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == [
#         {
#          "priority": 4,
#          "owner_id": 2,
#          "complete": False,
#          "title": "hair cut",
#          "description": "get a hair cut"
#         }
#     ]

# def test_read_one_authenticated(test_todo):
#     response = client.get("/todo/1")
#     print("response json:",response.json())
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == \
#         {
#             "id":1,
#             "title": 'Learn to code',
#             "description": 'Need to learn everyday',
#             "priority": 5,
#             "complete": False,
#             "owner_id":2
#         }

