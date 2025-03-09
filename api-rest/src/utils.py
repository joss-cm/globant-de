import pandas as pd
from fastapi import HTTPException
import io

def read_csv_file(file):
    """
    Lee un archivo CSV y lo convierte en un DataFrame de Pandas.
    """
    try:
        df = pd.read_csv(io.StringIO(file.file.read().decode("utf-8")))
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el archivo CSV: {str(e)}")

def validate_csv_columns(df, required_columns):
    """
    Valida que el DataFrame tenga las columnas necesarias.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Faltan columnas requeridas: {missing_columns}")
    return True
