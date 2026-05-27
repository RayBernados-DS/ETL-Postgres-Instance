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
# LOAD FUNCTION
# =========================================================
def load_presentation():

    try:

        print("\n===== STARTING LOAD PROCESS =====\n")

        # =====================================================
        # JAPAN
        # =====================================================
        print("Loading Japan sales data...")

        query_j = """
        SELECT
            s.invoice_id,
            s.product_id,
            s.quantity,
            s.date,
            i.product_name,
            i.category,
            i.price_usd
        FROM japan_sales_data s
        JOIN clean_japan_items i
        ON s.product_id = i.id
        """

        df_j = pd.read_sql(query_j, engine)

        df_j['total_usd'] = (
            df_j['price_usd'] *
            df_j['quantity']
        )

        df_j['country'] = 'Japan'

        # =====================================================
        # MYANMAR
        # =====================================================
        print("Loading Myanmar sales data...")

        query_m = """
        SELECT
            s.invoice_id,
            s.product_id,
            s.quantity,
            s.date,
            i.product_name,
            i.category,
            i.price_usd
        FROM myanmar_sales_data s
        JOIN clean_myanmar_items i
        ON s.product_id = i.id
        """

        df_m = pd.read_sql(query_m, engine)

        df_m['total_usd'] = (
            df_m['price_usd'] *
            df_m['quantity']
        )

        df_m['country'] = 'Myanmar'

        # =====================================================
        # FINAL CONSOLIDATION
        # =====================================================
        final_columns = [
            'invoice_id',
            'product_name',
            'category',
            'quantity',
            'total_usd',
            'country',
            'date'
        ]

        final_table = pd.concat(
            [
                df_j[final_columns],
                df_m[final_columns]
            ],
            ignore_index=True
        )

        # =====================================================
        # SAVE FINAL TABLE
        # =====================================================
        final_table.to_sql(
            "final_global_sales",
            engine,
            if_exists='replace',
            index=False
        )

        print("[SUCCESS] final_global_sales created")
        print(f"Rows loaded: {len(final_table)}")

        print("\n===== LOAD COMPLETE =====\n")

    except Exception as e:
        print("[ERROR] Load process failed")
        print(e)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    load_presentation()