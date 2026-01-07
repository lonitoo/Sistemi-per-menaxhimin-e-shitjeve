from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Sales Management System")

# Load CSV data
daily_sales = pd.read_csv("../../data/salesdaily.csv")

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.get("/sales/daily")
def get_daily_sales():
    return daily_sales.head(10).to_dict(orient="records")
