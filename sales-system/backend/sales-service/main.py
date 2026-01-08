from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
from datetime import date

app = FastAPI(title="Sales Management System")

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CSV_PATH = DATA_DIR / "sales_long.csv"

DATA_DIR.mkdir(exist_ok=True)

# Nëse file mungon, krijoje
if not CSV_PATH.exists():
    pd.DataFrame(
        columns=["date", "Year", "Month", "Hour", "weekday", "product_code", "quantity"]
    ).to_csv(CSV_PATH, index=False)


class Sale(BaseModel):
    product_code: str
    quantity: float


@app.get("/")
def root():
    return {"status": "Backend running"}


@app.get("/sales/long")
def get_sales_long():
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient="records")


