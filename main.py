from fastapi import FastAPI, Depends, HTTPException, Path,status
from pydantic import Field,BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from .database import engine
from .database import Base
from .routers import auth,todos,admin,user

app=FastAPI()

@app.get('/healthy')
def check_health():
    return {'status':'healthy'}

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
