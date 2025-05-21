from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
app = FastAPI()
DB_URL = os.getenv("DB_URL")

API_TOKEN = os.getenv("API_TOKEN")
engine = create_engine(DB_URL)

@app.get("/")
def status():
    return {"message": "API está online"}

# Middleware simples para verificar token
@app.middleware("http")
async def verificar_token(request: Request, call_next):
    if request.url.path.startswith("/pessoas"):  # Protege só esse endpoint (ou outros que quiser)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente ou inválido")

        token = auth_header.split(" ")[1]
        if token != API_TOKEN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token inválido")

    response = await call_next(request)
    return response

# Exemplo de endpoint protegido
@app.get("/pessoas")
def get_pessoas():
    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT COUNT(*) FROM pessoas", conn)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
