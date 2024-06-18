import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from database.tables import Base

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

def create_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)
