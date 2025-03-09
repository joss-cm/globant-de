import os
import pandas as pd
import logging
import itertools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
from src.models import Department, Job, HiredEmployee

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseCredentials:
    """Handles database credentials using environment variables."""
    def __init__(self):
        self.host = os.getenv("DB_HOST", "db")
        self.port = os.getenv("DB_PORT", "5432")
        self.name = os.getenv("DB_NAME", "testdb")
        self.user = os.getenv("DB_USER", "admin")
        self.password = os.getenv("DB_PASSWORD", "secret")

    def get_database_url(self):
        """Returns the database connection URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class DatabaseConnection:
    """Manages database connection using SQLAlchemy."""
    def __init__(self, credentials: DatabaseCredentials):
        self.engine = create_engine(credentials.get_database_url(), echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self):
        """Returns a new database session."""
        return self.SessionLocal()

class DataLoader:
    """Loads data into the database in batches."""
    def __init__(self, db_conn: DatabaseConnection):
        self.db_conn = db_conn

    def _load_data(self, csv_path, column_names, table, batch_size=1000):
        """
        Loads CSV data into the database in batches, avoiding duplicates.

        Parameters:
        - csv_path: Path to the CSV file.
        - column_names: List of column names (since CSV files have no headers).
        - table: Target database table.
        - batch_size: Number of rows per batch (default: 1000).
        """

        df = pd.read_csv(csv_path, names=column_names, header=None)

        # Replace NaN values with None
        df = df.where(pd.notnull(df), None)

        # Convert datetime if applicable
        if "datetime" in column_names:
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        # Drop rows with missing required fields
        df.dropna(subset=column_names, inplace=True)

        # Convert DataFrame to a list of dictionaries (records)
        data = df.to_dict(orient="records")

        # Insert data in batches
        with self.db_conn.engine.begin() as conn:
            batch_iterator = iter(data)
            while batch := list(itertools.islice(batch_iterator, batch_size)):  
                # Using `itertools.islice()` instead of a `for` loop improves memory efficiency 
                # This prevents excessive memory usage when handling large datasets.
                stmt = insert(table.__table__).values(batch).on_conflict_do_nothing(index_elements=["id"])
                conn.execute(stmt)

                # Log when exactly 1000 rows are inserted
                if len(batch) == batch_size:
                    logging.info(f"{batch_size} rows inserted into {table.__tablename__}")

        logging.info(f"{table.__tablename__.capitalize()} loaded successfully!")

def main():
    """Main function to load data from CSV files into the database."""

    credentials = DatabaseCredentials()
    db_connection = DatabaseConnection(credentials)
    loader = DataLoader(db_connection)

    # Define expected columns since CSV files have no headers
    columns_departments = ["id", "name"]
    columns_jobs = ["id", "name"]
    columns_employees = ["id", "name", "datetime", "department_id", "job_id"]

    try:
        loader._load_data("data/departments.csv", columns_departments, Department)
        loader._load_data("data/jobs.csv", columns_jobs, Job)
        loader._load_data("data/hired_employees.csv", columns_employees, HiredEmployee)

    except Exception as e:
        logging.error(f"Error loading CSV data: {e}")

if __name__ == "__main__":
    main()