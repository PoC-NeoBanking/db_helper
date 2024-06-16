from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import os
from dotenv import load_dotenv

# Loed environmental variables fgrom .env file
load_dotenv()

# Define the base class
Base = declarative_base()

# Define the User class mapped to the 'user' table
class User(Base):
    __tablename__ = 'user'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(255))
    lastName = Column(String(255))
    moneyAmount = Column(Float)
    lastTransactionTime = Column(DateTime)
    lastTransactionAmount = Column(Float)
    detectedFraudster = Column(Boolean)
    IPN = Column(Integer)

    # Relationship to transactions
    transactions = relationship("Transaction", back_populates="user")

# Define the Transaction class mapped to the 'transactions' table
class Transaction(Base):
    __tablename__ = 'transactions'
    userId = Column(Integer, ForeignKey('user.userId'), primary_key=True)
    transactionTime = Column(DateTime, primary_key=True)
    transactionAmount = Column(Float)

    # Relationship to user
    user = relationship("User", back_populates="transactions")


engine = create_engine(os.getenv('DATABASE_URL'))

# Create all tables in the engine
Base.metadata.create_all(engine)

# Example of creating a session
Session = sessionmaker(bind=engine)
session = Session()


session.commit()

# Close the session
session.close()
