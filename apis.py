from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import psycopg2
from sqlalchemy import create_engine, text

# Replace these values with your actual database connection details
def fetch_data(table_name):
    engine = create_engine('postgresql://fred:4004@localhost/699_project',isolation_level="AUTOCOMMIT")

    # Create a connection to the database
    with engine.connect() as connection:
        # Define the SQL SELECT statement
        select_query = text(f"SELECT * FROM {table_name}")

        # Execute the query and fetch the results
        result = connection.execute(select_query)

        # Fetch all rows
    rows = result.fetchall()

    # Make the data into List of lists
    data = [list(row) for row in rows]
    
    ##Convert the data into list of dicts
    # column_names = result.keys()
    # data = [dict(zip(column_names, row)) for row in rows]

    return data

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get_data/computer_software")
def get_data():
    #Calling function to fetch data form database
    data = fetch_data("computer_software")
    return {"data": data}

@app.get("/get_data/steel")
def get_data():
    #Calling function to fetch data form database
    data = fetch_data("steel")
    return {"data": data}