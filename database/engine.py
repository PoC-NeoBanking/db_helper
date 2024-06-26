import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.tables import Base

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
