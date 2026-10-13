import pandas as pd
from pathlib import Path

# Step 1: Locate the original dataset
raw_folder = Path("data/raw")
output_folder = Path("data/cleaned")

files = (
    list(raw_folder.glob("*.xls"))
    + list(raw_folder.glob("*.xlsx"))
)

if not files:
    raise FileNotFoundError(
        "No Excel dataset found in data/raw."
    )

file_path = files[0]
df = pd.read_excel(file_path)

print("Original file:", file_path.name)
print("Original rows:", len(df))

# Step 2: Clean column names
df.columns = df.columns.str.strip()

# Step 3: Remove exact duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print("Duplicate rows removed:", duplicates)

# Step 4: Standardize text fields
text_columns = [
    "Order ID",
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "Country/Region",
    "City",
    "State/Province",
    "Region",
    "Product ID",
    "Category",
    "Sub-Category",
    "Product Name",
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].str.strip()

# Step 5: Validate date columns
for column in ["Order Date", "Ship Date"]:
    df[column] = pd.to_datetime(
        df[column], errors="coerce"
    )

# Step 6: Validate numeric columns
numeric_columns = [
    "Row ID",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# Step 7: Check data quality
print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nInvalid date values:")
print(df[["Order Date", "Ship Date"]].isnull().sum())

print("\nRows where shipping date is before order date:")
print((df["Ship Date"] < df["Order Date"]).sum())

# Step 8: Save the cleaned dataset
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "cleaned_sales.csv"
df.to_csv(output_file, index=False)

print("\nFinal rows:", len(df))
print("Final columns:", len(df.columns))
print("Cleaned dataset saved to:", output_file)