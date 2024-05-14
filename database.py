from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#added postgresql database
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pepsodent123@localhost/TodoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = 'sqlite:///./TodosApp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()