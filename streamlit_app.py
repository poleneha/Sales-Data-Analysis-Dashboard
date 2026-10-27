from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Data Analysis Dashboard")
st.caption("Superstore sales, profit, product and regional performance")

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"

@st.cache_data
def load_data():
    # Prefer cleaned CSV files; otherwise try CSV and Excel files.
    files = []
    for folder in [DATA_DIR / "cleaned", DATA_DIR / "raw", DATA_DIR]:
        if folder.exists():
            files.extend(folder.glob("*.csv"))

    if files:
        return pd.read_csv(files[0])

    for folder in [DATA_DIR / "cleaned", DATA_DIR / "raw", DATA_DIR]:
        if folder.exists():
            for pattern in ["*.xlsx", "*.xls"]:
                matches = list(folder.glob(pattern))
                if matches:
                    return pd.read_excel(matches[0])

    return None

df = load_data()

if df is None:
    st.error(
        "No dataset found. Add your cleaned CSV to data/cleaned "
        "and commit it to GitHub."
    )
    st.stop()

df.columns = df.columns.str.strip()

# Identify common column names
def find_col(*names):
    return next((n for n in names if n in df.columns), None)

sales_col = find_col("Sales", "sales")
profit_col = find_col("Profit", "profit")
order_col = find_col("Order ID", "Order_ID", "order_id")
date_col = find_col("Order Date", "Order_Date", "order_date")
region_col = find_col("Region", "region")
category_col = find_col("Category", "category")
product_col = find_col("Product Name", "Product_Name", "product_name")
quantity_col = find_col("Quantity", "quantity")

if sales_col is None:
    st.error("I couldn't find a Sales column. Please check your dataset.")
    st.write("Columns found:", df.columns.tolist())
    st.stop()

# Filters
filtered = df.copy()
with st.sidebar:
    st.header("Dashboard Filters")

    if region_col:
        regions = sorted(filtered[region_col].dropna().unique().tolist())
        selected_regions = st.multiselect(
            "Region", regions, default=regions
        )
        filtered = filtered[filtered[region_col].isin(selected_regions)]

    if category_col:
        categories = sorted(filtered[category_col].dropna().unique().tolist())
        selected_categories = st.multiselect(
            "Category", categories, default=categories
        )
        filtered = filtered[
            filtered[category_col].isin(selected_categories)
        ]

sales = filtered[sales_col].sum()
profit = filtered[profit_col].sum() if profit_col else 0
orders = filtered[order_col].nunique() if order_col else len(filtered)
units = filtered[quantity_col].sum() if quantity_col else None

a, b, c, d = st.columns(4)
a.metric("Total Sales", f"${sales:,.2f}")
b.metric("Total Profit", f"${profit:,.2f}" if profit_col else "N/A")
c.metric("Orders", f"{orders:,.0f}")
d.metric("Units Sold", f"{units:,.0f}" if units is not None else "N/A")

left, right = st.columns(2)

with left:
    if region_col:
        st.subheader("Sales by Region")
        chart = filtered.groupby(region_col, as_index=False)[sales_col].sum()
        st.plotly_chart(
            px.bar(chart, x=region_col, y=sales_col, title="Regional Sales"),
            use_container_width=True,
        )

with right:
    if category_col:
        st.subheader("Sales by Category")
        chart = filtered.groupby(category_col, as_index=False)[sales_col].sum()
        st.plotly_chart(
            px.pie(chart, names=category_col, values=sales_col,
                   title="Category Sales", hole=0.4),
            use_container_width=True,
        )

if date_col:
    st.subheader("Sales Trend Over Time")
    dates = pd.to_datetime(filtered[date_col], errors="coerce")
    trend_data = filtered.assign(Month=dates.dt.to_period("M").astype(str))
    trend_data = trend_data[trend_data["Month"] != "NaT"]
    if not trend_data.empty:
        trend = trend_data.groupby("Month", as_index=False)[sales_col].sum()
        st.plotly_chart(
            px.line(trend, x="Month", y=sales_col, markers=True),
            use_container_width=True,
        )

if product_col:
    st.subheader("Top 10 Products by Sales")
    top = (
        filtered.groupby(product_col, as_index=False)[sales_col]
        .sum()
        .nlargest(10, sales_col)
    )
    st.plotly_chart(
        px.bar(top, x=sales_col, y=product_col, orientation="h"),
        use_container_width=True,
    )

st.subheader("Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)