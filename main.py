# import necessary libraries
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List


# Database configuration
DATABASE_URL = "postgresql://neondb_owner:npg_XlZt6MW0JhYR@ep-purple-base-a8nvg3hc-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
