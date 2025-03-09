from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from src.database import get_db
from src.models import Department, Job, HiredEmployee

router = APIRouter()

TABLE_MAPPING = {
    "departments": {"model": Department, "columns": ["id", "name"]},
    "jobs": {"model": Job, "columns": ["id", "name"]},
    "hired_employees": {"model": HiredEmployee, "columns": ["id", "name", "datetime", "department_id", "job_id"]}
}

@router.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """API endpoint to upload CSV files to a specified table"""
    
    if table_name not in TABLE_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid table name")

    table_info = TABLE_MAPPING[table_name]
    model = table_info["model"]
    required_columns = table_info["columns"]

    try:
        df = pd.read_csv(file.file, names=required_columns, header=None)
        validate_csv_columns(df, required_columns)
        if "datetime" in required_columns:
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        df.dropna(subset=required_columns, inplace=True)
        records = [model(**row) for row in df.to_dict(orient="records")]
        db.bulk_save_objects(records)
        db.commit()

        return {"message": f"{len(records)} rows uploaded successfully to {table_name}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error uploading CSV: {str(e)}")

def validate_csv_columns(df: pd.DataFrame, required_columns: list):
    """Validates if all required columns are present in the DataFrame"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {missing_columns}")