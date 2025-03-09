from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "API is running!"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        # Intenta hacer una consulta simple para verificar la conexión
        db.execute("SELECT 1")
        return {"message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")