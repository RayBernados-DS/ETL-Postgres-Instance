from extract import load_csv
from transform import transform_data
from load import load_presentation

def run_pipeline():

    print("\n========== ETL PIPELINE START ==========\n")

    load_csv()

    transform_data()

    load_presentation()

    print("\n========== ETL PIPELINE COMPLETE ==========\n")

if __name__ == "__main__":
    run_pipeline()