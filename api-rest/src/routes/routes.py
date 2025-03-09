from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from src.database import get_db
from src.models import Department, Job, HiredEmployee

router = APIRouter()

@router.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    
    if table_name == "departments":
        required_columns = ["id", "name"]
        validate_csv_columns(df, required_columns)

        departments = [Department(id=row["id"], name=row["name"]) for _, row in df.iterrows()]
        db.bulk_save_objects(departments)

    elif table_name == "jobs":
        required_columns = ["id", "name"]
        validate_csv_columns(df, required_columns)

        jobs = [Job(id=row["id"], name=row["name"]) for _, row in df.iterrows()]
        db.bulk_save_objects(jobs)

    elif table_name == "hired_employees":
        required_columns = ["id", "name", "datetime", "department_id", "job_id"]
        validate_csv_columns(df, required_columns)

        employees = [
            HiredEmployee(
                id=row["id"],
                name=row["name"],
                datetime=row["datetime"],
                department_id=row["department_id"],
                job_id=row["job_id"]
            ) for _, row in df.iterrows()
        ]
        db.bulk_save_objects(employees)
    else:
        raise HTTPException(status_code=400, detail="Invalid table name")

    db.commit()
    return {"message": f"CSV uploaded successfully to {table_name}"}

def validate_csv_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {missing_columns}")