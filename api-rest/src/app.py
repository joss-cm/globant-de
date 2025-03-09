from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "API is running!"}
