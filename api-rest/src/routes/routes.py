from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Department, Job, HiredEmployee
from src.utils import read_csv_file, validate_csv_columns

router = APIRouter()

@router.post("/upload/{table_name}")
def upload_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = read_csv_file(file)
        
        if table_name == "departments":
            validate_csv_columns(df, ["id", "name"])
            db.bulk_save_objects([Department(**row) for row in df.to_dict(orient="records")])

        elif table_name == "jobs":
            df.columns = df.columns.str.strip()
            validate_csv_columns(df, ["id", "name"])
            for _, row in df.iterrows():
                db.add(Job(id=row["id"], name=row["name"]))

        elif table_name == "hired_employees":
            df.columns = df.columns.str.lower()
            validate_csv_columns(df, ["id", "name", "datetime", "department_id", "job_id"])
            for _, row in df.iterrows():
                db.add(HiredEmployee(
                    id=row["id"],
                    name=row["name"],
                    datetime=row["datetime"],
                    department_id=row["department_id"],
                    job_id=row["job_id"]
                ))
        else:
            raise HTTPException(status_code=400, detail=f"Unknown table name: {table_name}")

        db.commit()
        return {"message": f"Data successfully loaded into {table_name}"}

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))