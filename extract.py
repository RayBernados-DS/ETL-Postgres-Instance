import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# =========================================================
# DATABASE CONNECTION
# Render automatically provides DATABASE_URL
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not found.")

# Create PostgreSQL engine
engine = create_engine(DATABASE_URL)

# =========================================================
# PROJECT ROOT DIRECTORY
# This makes the script work on Render deployment
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Source CSV folder
BASE_PATH = os.path.join(BASE_DIR, "data", "source")

# =========================================================
# CSV CONFIGURATION
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
# EXTRACT CSV TO POSTGRESQL
# =========================================================
def load_csv():

    print("\n===================================")
    print("STARTING EXTRACTION PROCESS")
    print("===================================\n")

    total_files = 0
    successful_files = 0
    failed_files = 0

    # Loop through folders
    for folder_name, files in STAGING_CONFIGS.items():

        print(f"\nProcessing folder: {folder_name}")

        # Build folder path
        folder_path = os.path.join(BASE_PATH, folder_name)

        # Check if folder exists
        if not os.path.exists(folder_path):
            print(f"[ERROR] Folder not found: {folder_path}")
            continue

        # Process each CSV file
        for file_name in files:

            total_files += 1

            full_path = os.path.join(folder_path, file_name)

            print(f"\nReading: {file_name}")

            # Check file existence
            if not os.path.exists(full_path):
                print(f"[ERROR] File not found: {full_path}")
                failed_files += 1
                continue

            try:

                # =================================================
                # READ CSV
                # =================================================
                df = pd.read_csv(full_path)

                # =================================================
                # CLEAN COLUMN NAMES
                # =================================================
                df = clean_column_names(df)

                # =================================================
                # REMOVE DUPLICATES
                # =================================================
                df = df.drop_duplicates()

                # =================================================
                # GENERATE TABLE NAME
                # =================================================
                table_name = (
                    file_name
                    .replace(".csv", "")
                    .lower()
                )

                # =================================================
                # LOAD TO POSTGRESQL
                # =================================================
                df.to_sql(
                    table_name,
                    engine,
                    if_exists='replace',
                    index=False
                )

                print(f"[SUCCESS] Uploaded table: {table_name}")
                print(f"Rows inserted: {len(df)}")

                successful_files += 1

            except pd.errors.EmptyDataError:
                print(f"[FAILED] Empty CSV file: {file_name}")
                failed_files += 1

            except pd.errors.ParserError as e:
                print(f"[FAILED] CSV parsing error in {file_name}")
                print(f"Reason: {e}")
                failed_files += 1

            except SQLAlchemyError as e:
                print(f"[FAILED] Database error while uploading {file_name}")
                print(f"Reason: {e}")
                failed_files += 1

            except Exception as e:
                print(f"[FAILED] Unexpected error in {file_name}")
                print(f"Reason: {e}")
                failed_files += 1

    # =========================================================
    # FINAL SUMMARY
    # =========================================================
    print("\n===================================")
    print("EXTRACTION SUMMARY")
    print("===================================")

    print(f"Total files processed : {total_files}")
    print(f"Successful uploads    : {successful_files}")
    print(f"Failed uploads        : {failed_files}")

    print("\nEXTRACTION FINISHED\n")

# =========================================================
# MAIN EXECUTION
# =========================================================
if __name__ == "__main__":
    load_csv()