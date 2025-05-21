import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

API_TOKEN = os.getenv("API_TOKEN")

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
    return [{"nome": "João"}, {"nome": "Maria"}]
