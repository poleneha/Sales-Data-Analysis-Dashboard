import pandas as pd
from pathlib import Path

# Find the original sales dataset
data_folder = Path("data/raw")
files = list(data_folder.glob("*.xls")) + list(data_folder.glob("*.xlsx"))

if not files:
    print("No Excel dataset found in data/raw.")
else:
    file_path = files[0]
    print("Dataset:", file_path.name)

    # Read the Excel file
    df = pd.read_excel(file_path)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset shape (rows, columns):")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())