import pandas as pd
import sqlite3
import os

def load_csv():
    # 1. Set the root path where your CSV folders are located
    # Ensure this matches the folder where you are running the script
    base_path = r"C:\Users\phant\OneDrive\Documents\ADMS Final\Data\source"
    
    # Configuration: Mapping Databases to their specific subfolders and files
    staging_configs = {
        "japan staging area.db": {
            "folder": "japan_store",
            "files": [
                "japan_branch.csv", 
                "japan_Customers.csv", 
                "japan_items.csv", 
                "japan_payment.csv", 
                "japan_sales_data.csv"
            ]
        },
        "myanmar staging area.db": {
            "folder": "myanmar_store",
            "files": [
                "myanmar_branch.csv", 
                "myanmar_customers.csv", 
                "myanmar_items.csv", 
                "myanmar_payment.csv", 
                "myanmar_sales_data.csv"
            ]
        }
    }

    print("--- Starting Extraction ---\n")

    for db_name, config in staging_configs.items():
        # Connect to the database file (created in the same folder as the script)
        conn = sqlite3.connect(db_name)
        folder_name = config["folder"]
        
        print(f"Checking Database: {db_name}")

        for file_name in config["files"]:
            # Construct the full path to the CSV file
            full_path = os.path.join(base_path, folder_name, file_name)

            if not os.path.exists(full_path):
                print(f" [ERROR] Not found: {full_path}")
                continue

            try:
                # Load CSV
                df = pd.read_csv(full_path)
                
                # Create table name from filename
                table_name = file_name.replace(".csv", "").lower()
                
                # Write to SQL
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                
                # Success Verification
                db_count = pd.read_sql_query(f"SELECT COUNT(*) FROM `{table_name}`", conn).iloc[0, 0]
                print(f" [SUCCESS] Extracted {file_name} -> {db_count} rows.")

            except Exception as e:
                print(f" [FAILED] {file_name}: {e}")

        conn.close()
        print(f"Finished {db_name}\n")

if __name__ == "__main__":
    load_csv()