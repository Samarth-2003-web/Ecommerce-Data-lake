import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
base_dir = Path(__file__).resolve().parents[1]
bronze_path = base_dir / "data" / "bronze" / "E-com_Data.xlsx"
silver_dir = base_dir / "data" / "silver"
silver_dir.mkdir(parents=True, exist_ok=True)


df = pd.read_excel(bronze_path)

print("Original shape:", df.shape)

df.drop_duplicates(inplace=True)

df = df.dropna(subset=["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice"])
