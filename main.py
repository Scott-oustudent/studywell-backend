import os
import mysql.connector
from flask import Flask
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Function to get a database connection
def get_db_connection():
    try:
        # The Cloud SQL Auth Proxy exposes the database on localhost
        conn = mysql.connector.connect(
            host='127.0.0.1', # Connect to the local Cloud SQL Auth Proxy
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        return conn
    except mysql.connector.Error as e:
        # Use logging.exception to get the full traceback
        logging.exception("Error connecting to MySQL:")
        return None

# The rest of your app routes remain the same
@app.route("/")
def home():
    return "Backend is running!"

@app.route("/check_db")
def check_db():
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "success", "message": "Database connection successful!"}
    else:
        return {"status": "error", "message": "Failed to connect to the database."}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))