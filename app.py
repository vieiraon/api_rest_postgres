from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

app = FastAPI()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

@app.get("/")
def home():
    return {"message": "API está ativo"}

@app.get("/pessoas")
def get_pessoas():
    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT ch_pessoa FROM pessoas LIMIT 10", conn)
        return df.to_dict(orient="records")
    except SQLAlchemyError as e:
        return {"error": str(e)}
