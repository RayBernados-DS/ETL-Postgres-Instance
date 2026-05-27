import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# =========================================================
# DATABASE CONNECTION
# =========================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgresql_etl_eph8_user:uZ5XeN5IokS7oN0DnCNp1JGXzezLtvqQ@dpg-d8b6phel51nc739dqrs0-a.singapore-postgres.render.com/postgresql_etl_eph8"
)

engine = create_engine(DATABASE_URL)

# =========================================================
# PROJECT DIRECTORY
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = os.path.join(BASE_DIR, "data", "source")

# =========================================================
# CSV CONFIGS
# =========================================================
STAGING_CONFIGS = {

    "japan_store": [
        "japan_branch.csv",
        "japan_Customers.csv",
        "japan_items.csv",
        "japan_payment.csv",
        "japan_sales_data.csv"
    ],

    "myanmar_store": [
        "myanmar_branch.csv",
        "myanmar_customers.csv",
        "myanmar_items.csv",
        "myanmar_payment.csv",
        "myanmar_sales_data.csv"
    ]
}

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================
def clean_column_names(df):

    df.columns = (
        df.columns
        .str.replace("'", "", regex=False)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

# =========================================================
# EXTRACT FUNCTION
# =========================================================
def load_csv():

    print("\n===== STARTING EXTRACTION =====\n")

    for folder_name, files in STAGING_CONFIGS.items():

        folder_path = os.path.join(BASE_PATH, folder_name)

        print(f"\nProcessing folder: {folder_name}")

        for file_name in files:

            full_path = os.path.join(folder_path, file_name)

            if not os.path.exists(full_path):
                print(f"[ERROR] Missing file: {full_path}")
                continue

            try:

                df = pd.read_csv(full_path)

                # Clean columns immediately
                df = clean_column_names(df)

                # Remove duplicates
                df = df.drop_duplicates()

                table_name = (
                    file_name
                    .replace(".csv", "")
                    .lower()
                )

                df.to_sql(
                    table_name,
                    engine,
                    if_exists='replace',
                    index=False
                )

                print(f"[SUCCESS] {table_name} uploaded")
                print(f"Rows inserted: {len(df)}")

            except SQLAlchemyError as e:
                print(f"[DATABASE ERROR] {file_name}")
                print(e)

            except Exception as e:
                print(f"[FAILED] {file_name}")
                print(e)

    print("\n===== EXTRACTION COMPLETE =====\n")

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    load_csv()
