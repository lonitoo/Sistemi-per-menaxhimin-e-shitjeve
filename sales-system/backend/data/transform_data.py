import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "salesdaily.csv"
OUTPUT_CSV = BASE_DIR / "sales_long.csv"

# Lexo dataset-in
df = pd.read_csv(INPUT_CSV)

# Kolonat që NUK janë produkte
meta_cols = ["datum", "Year", "Month", "Hour", "Weekday Name"]

# Produktet (të gjitha kolonat tjera)
product_cols = [c for c in df.columns if c not in meta_cols]

# Transformim WIDE ➜ LONG
df_long = df.melt(
    id_vars=meta_cols,
    value_vars=product_cols,
    var_name="product_code",
    value_name="quantity"
)

# Largo vlerat 0
df_long = df_long[df_long["quantity"] > 0]

# Rename për standard
df_long = df_long.rename(columns={
    "datum": "date",
    "Weekday Name": "weekday"
})

# Ruaje rezultatin
df_long.to_csv(OUTPUT_CSV, index=False)

print("✅ Transformimi përfundoi me sukses")
print("📁 File i ri:", OUTPUT_CSV)
