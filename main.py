import os
import psycopg2
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Function to get a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            dbname=os.environ.get("DB_NAME")
        )
        return conn
    except psycopg2.Error as e:
        logging.exception("Error connecting to PostgreSQL:")
        return None

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/check_db")
def check_db():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "success", "message": "Database connection successful!"})
    else:
        return jsonify({"status": "error", "message": "Failed to connect to the database."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))