import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Department, Job, HiredEmployee
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "testdb")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

from src.models import Department, Job, HiredEmployee

def load_departments(session, csv_path):
    df = pd.read_csv(csv_path, names=["id", "department"], header=None)
    for _, row in df.iterrows():
        dept = Department(id=int(row["id"]), name=row["department"])
        session.merge(dept)
    session.commit()

def load_jobs(session, csv_path):
    df = pd.read_csv(csv_path, names=["id", "job"], header=None)
    for _, row in df.iterrows():
        job = Job(id=row["id"], name=row["job"])
        session.merge(job)
    session.commit()

def load_employees(session, csv_path):
    df = pd.read_csv(csv_path, names=["id", "name", "datetime", "department_id", "job_id"], header=None)
    df = df.where(pd.notnull(df), None) 

    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df.dropna(subset=["id", "name", "datetime", "department_id", "job_id"], inplace=True)

    for _, row in df.iterrows():
        if pd.isna(row['datetime']):
            continue

        employee = HiredEmployee(
            id=row["id"], 
            name=row["name"],
            datetime=pd.to_datetime(row["datetime"]),
            department_id=int(row["department_id"]) if pd.notnull(row["department_id"]) else None, 
            job_id=int(row["job_id"]) if pd.notnull(row["job_id"]) else None
        )
        session.merge(employee)
    session.commit()


if __name__ == "__main__":
    import pandas as pd

    session = SessionLocal()

    try:
        load_departments(session, "data/departments.csv")
        print("Departments loaded successfully!")

        load_jobs(session, "data/jobs.csv")
        print("Jobs loaded successfully!")

        load_employees(session, "data/hired_employees.csv")
        print("Hired employees loaded successfully!")

    except Exception as e:
        print("Error loading CSV data:", e)
    finally:
        session.close()