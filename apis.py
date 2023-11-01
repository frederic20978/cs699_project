from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import psycopg2

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get_data/computer_software")
def get_data():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="699_project",
        user="fred",
        password="4004",
        host="localhost"
    )

    cursor = conn.cursor()

    # Fetch data
    cursor.execute("SELECT * FROM stock_data")
    data = cursor.fetchall()

    conn.close()

    return {"data": data}