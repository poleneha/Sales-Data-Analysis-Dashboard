import pandas as pd
from pathlib import Path

# Step 1: Load the cleaned dataset
file_path = Path("data/cleaned/cleaned_sales.csv")
df = pd.read_csv(file_path)

# Step 2: Prepare date column
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Step 3: Calculate key performance indicators (KPIs)
total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
total_products = df["Product ID"].nunique()
total_customers = df["Customer ID"].nunique()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

print("=" * 45)
print("       SALES DATA ANALYSIS REPORT")
print("=" * 45)

print(f"Total Sales:     ${total_sales:,.2f}")
print(f"Total Orders:    {total_orders:,}")
print(f"Unique Products: {total_products:,}")
print(f"Customers:       {total_customers:,}")
print(f"Total Profit:    ${total_profit:,.2f}")
print(f"Units Sold:      {total_quantity:,}")

# Step 4: Monthly sales analysis
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Month", as_index=False)["Sales"]
    .sum()
    .sort_values("Month")
)

print("\nMONTHLY SALES")
print(monthly_sales.to_string(index=False))

# Step 5: Top 10 products by sales
top_products = (
    df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUCTS BY SALES")
print(top_products.to_string(index=False))

# Step 6: Regional sales analysis
regional_sales = (
    df.groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

print("\nREGIONAL SALES")
print(regional_sales.to_string(index=False))

# Step 7: Category sales analysis
category_sales = (
    df.groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

print("\nCATEGORY SALES")
print(category_sales.to_string(index=False))

# Step 8: Save analysis results
output_folder = Path("reports")
output_folder.mkdir(parents=True, exist_ok=True)

monthly_sales.to_csv(output_folder / "monthly_sales.csv", index=False)
top_products.to_csv(output_folder / "top_products.csv", index=False)
regional_sales.to_csv(output_folder / "regional_sales.csv", index=False)
category_sales.to_csv(output_folder / "category_sales.csv", index=False)

print("\nAnalysis completed successfully!")
print("Analysis results saved in the reports folder.")