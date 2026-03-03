from fastapi import FastAPI
from app.routers import proxy

app = FastAPI(title="API Gateway")

app.include_router(proxy.router)

@app.get("/")
def health():
    return {"status": "API Gateway Running on 8000"}