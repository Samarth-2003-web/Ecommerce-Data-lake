import pandas as pd
from pathlib import Path

# Paths
base_dir = Path(__file__).resolve().parents[1]
silver_path = base_dir / "data" / "silver" / "orders_cleaned.parquet"
gold_dir = base_dir / "data" / "gold"
gold_dir.mkdir(parents=True, exist_ok=True)

# Load cleaned data
df = pd.read_parquet(silver_path)

# -----------------------------
# DIM PRODUCTS
# -----------------------------
dim_products = (
    df[["Item Code"]]
    .drop_duplicates()
    .rename(columns={
        "Item Code": "product_id"
    })
)

dim_products.to_csv(gold_dir / "dim_products.csv", index=False)
print("Saved:", gold_dir / "dim_products.csv")

# -----------------------------
# DIM CUSTOMERS
# -----------------------------
dim_customers = (
    df[["CustomerID"]]
    .dropna()
    .drop_duplicates()
    .rename(columns={
        "CustomerID": "customer_id"
    })
)

dim_customers.to_csv(gold_dir / "dim_customers.csv", index=False)
print("Saved:", gold_dir / "dim_customers.csv")

# -----------------------------
# DIM LOCATIONS
# -----------------------------
dim_locations = (
    df[["Shipping Location"]]
    .drop_duplicates()
    .rename(columns={
        "Shipping Location": "location"
    })
)

dim_locations.to_csv(gold_dir / "dim_locations.csv", index=False)
print("Saved:", gold_dir / "dim_locations.csv")

# -----------------------------
# FACT ORDERS
# -----------------------------
fact_orders = df.rename(columns={
    "InvoieNo": "order_id",
    "Item Code": "product_id",
    "CustomerID": "customer_id",
    "Date of purchase": "order_date",
    "Quantity": "quantity",
    "price per Unit": "unit_price",
    "Price": "total_amount",
    "Shipping Location": "location",
    "Cancelled_status": "is_cancelled"
})

fact_orders = fact_orders[[
    "order_id", "order_date", "Time", "customer_id",
    "product_id", "quantity", "unit_price", "total_amount",
    "location", "is_cancelled"
]]

fact_orders.to_csv(gold_dir / "fact_orders.csv", index=False)
print("Saved:", gold_dir / "fact_orders.csv")
