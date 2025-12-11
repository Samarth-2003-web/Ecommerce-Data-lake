import pandas as pd
from pathlib import Path

# set paths
base_dir = Path(__file__).resolve().parents[1]
bronze_path = base_dir / "data" / "bronze" / "E-com_Data.xlsx"

print("Reading:", bronze_path)

df = pd.read_excel(bronze_path)

print("Shape (rows, columns):", df.shape)
print("\nColumns:\n", df.columns)

print("\nSample rows:")
print(df.head(5))


data = df.drop(['Sold as set', 'Reason of return'], axis=1)

# Clean the data
# Remove duplicates
data = data.drop_duplicates()

# Fill missing values in Cancelled_status with False before cleaning
data['Cancelled_status'] = data['Cancelled_status'].fillna(False)

# Strip whitespace from string columns (only if they actually contain strings)
for col in data.columns:
    if data[col].dtype == "object":
        data[col] = data[col].astype(str).str.strip()

# Handle missing values (drop rows with NaN in critical columns)
data = data.dropna()

print(data.head(5))
print(f"\nCleaned data shape: {data.shape}")

silver_dir = base_dir / "data" / "silver"
silver_dir.mkdir(parents=True, exist_ok=True)
silver_file = silver_dir / "orders_cleaned.parquet"
data.to_parquet(silver_file, index=False)

print("\nSaved cleaned data to:", silver_file)