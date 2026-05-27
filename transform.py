import pandas as pd
import os
from sqlalchemy import create_engine

# =========================================================
# DATABASE CONNECTION
# =========================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://db_nako_user:3halkU77mrx0Gaw8HxpVqoDGDDNSDCpc@dpg-d7ngs4vlk1mc73d4p9m0-a.singapore-postgres.render.com/db_nako?sslmode=require"
)

engine = create_engine(DATABASE_URL)

# =========================================================
# TRANSFORMATION FUNCTION
# =========================================================
def transform_data():

    try:

        print("\n===== STARTING TRANSFORMATION =====\n")

        # =====================================================
        # JAPAN
        # =====================================================
        print("Transforming Japan items...")

        df_j = pd.read_sql(
            "SELECT * FROM japan_items",
            engine
        )

        df_j.columns = df_j.columns.str.strip()

        df_j['product_name'] = (
            df_j['product_name']
            .astype(str)
            .str.strip()
        )

        # Currency conversion
        df_j['price_usd'] = df_j['price'] * 0.0065

        # Remove duplicates
        df_j = df_j.drop_duplicates()

        df_j.to_sql(
            "clean_japan_items",
            engine,
            if_exists='replace',
            index=False
        )

        print("[SUCCESS] clean_japan_items created")

        # =====================================================
        # MYANMAR
        # =====================================================
        print("Transforming Myanmar items...")

        df_m = pd.read_sql(
            "SELECT * FROM myanmar_items",
            engine
        )

        df_m.columns = df_m.columns.str.strip()

        df_m['name'] = (
            df_m['name']
            .astype(str)
            .str.strip()
        )

        # Standardize schema
        df_m = df_m.rename(columns={
            'name': 'product_name',
            'type': 'category'
        })

        # Myanmar already USD
        df_m['price_usd'] = df_m['price']

        # Remove duplicates
        df_m = df_m.drop_duplicates()

        df_m.to_sql(
            "clean_myanmar_items",
            engine,
            if_exists='replace',
            index=False
        )

        print("[SUCCESS] clean_myanmar_items created")

        print("\n===== TRANSFORMATION COMPLETE =====\n")

    except Exception as e:
        print(f"[ERROR] Transformation failed")
        print(e)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    transform_data()