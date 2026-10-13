import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create output folder
output_folder = Path("reports")
output_folder.mkdir(parents=True, exist_ok=True)

# Load analysis results
monthly = pd.read_csv(output_folder / "monthly_sales.csv")
products = pd.read_csv(output_folder / "top_products.csv")
regions = pd.read_csv(output_folder / "regional_sales.csv")
categories = pd.read_csv(output_folder / "category_sales.csv")

# Chart 1: Monthly Sales Trend
plt.figure(figsize=(12, 5))
plt.plot(monthly["Month"], monthly["Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "monthly_sales_trend.png", dpi=150)
plt.close()

# Chart 2: Top 10 Products
plt.figure(figsize=(12, 6))
plt.barh(products["Product Name"], products["Sales"])
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(output_folder / "top_products.png", dpi=150)
plt.close()

# Chart 3: Regional Sales
plt.figure(figsize=(8, 5))
plt.bar(regions["Region"], regions["Sales"])
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(output_folder / "regional_sales.png", dpi=150)
plt.close()

# Chart 4: Category Sales
plt.figure(figsize=(8, 5))
plt.bar(categories["Category"], categories["Sales"])
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(output_folder / "category_sales.png", dpi=150)
plt.close()

print("All four charts created successfully!")
print("Charts saved in the reports folder.")