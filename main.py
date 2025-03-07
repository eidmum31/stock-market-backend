# import necessary libraries
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List


# Postgresql Database configuration which is hosted in neon
DATABASE_URL = "postgresql://neondb_owner:npg_XlZt6MW0JhYR@ep-purple-base-a8nvg3hc-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Stock model
class Stock(Base):
    __tablename__ = "stockData"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    trade_code = Column(String, index=True)
    high = Column(String)
    low = Column(String)
    open = Column(String)
    close = Column(String)
    volume = Column(String)


# Create the stocks table
Base.metadata.create_all(bind=engine)

# Pydantic models
class StockBase(BaseModel):
    date: str
    trade_code: str
    high:str
    low:str
    open:str
    close:str
    volume:str

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    id: int

    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def welcome():
    return {"message": "Welcome to my FastAPI application"}


# get all the stocks
@app.get("/stocks", response_model=List[StockResponse])
def read_stocks(skip: int = 0, db: Session = Depends(get_db)):

    stocks = db.query(Stock).offset(skip).all()
    return stocks
