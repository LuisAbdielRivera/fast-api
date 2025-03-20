from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);
base = declarative_base();