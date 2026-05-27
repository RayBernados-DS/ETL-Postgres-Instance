import os
from flask import Flask, jsonify
import extract
import transform
import load

app = Flask(__name__)

@app.route('/')
def home():
    return "ETL Pipeline Server is Running Live!"

@app.route('/run-pipeline', methods=['GET', 'POST'])
def trigger_pipeline():
    try:
        print("🚀 Remote trigger received! Starting Cloud ETL Pipeline...")
        
        # Run your fixed functions sequentially
        extract.load_csv()
        transform.clean_sqlite_table()
        load.load_presentation()
        
        return jsonify({"status": "success", "message": "Pipeline executed successfully in the cloud!"}), 200
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == "__main__":
    # Render binds to the PORT environment variable automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)