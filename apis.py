from fastapi import FastAPI
import numpy as np
from fastapi.staticfiles import StaticFiles
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
    #prefernce list
    preference = [0, -3, 0, 1, 1, 0, 1, 0, 2]

    # Separate the names and the numeric data
    numeric_data = [entry[1:] for entry in data]

    # Convert the numeric data to a numpy array
    numeric_data = np.array(numeric_data)

    total_mrkt_cap = sum(entry[2] for entry in data)

    for entry in data:
    # Update 'np_qtr' normalising with market cap
        entry[4] = entry[4] / (100 * (entry[2] / total_mrkt_cap))

    for entry in data:
    # Update 'np_qtr' normalising with market cap
        entry[6] = entry[6] / (100 * (entry[2] / total_mrkt_cap))
   
    # Normalize the numeric data
    data_normalized = (numeric_data - np.min(numeric_data, axis=0)) / (np.max(numeric_data, axis=0) - np.min(numeric_data, axis=0)) 

    # Calculate the score for each stock
    scores = np.sum(data_normalized * preference, axis=1)

    #normalize
    softmax_scores = np.exp(scores) / np.sum(np.exp(scores), axis=0)

    # Combine the scores with the stock names
    data_scored = list(zip(np.array(data)[:, 0], softmax_scores))

    # Sort the stocks by score
    data_scored.sort(key=lambda x: x[1], reverse=True)

    return {"data": data,"preference":data_scored}

@app.get("/get_data/steel")
def get_data():
    #Calling function to fetch data form database
    data = fetch_data("steel")
    #prefernce list
    preference = [0, -3, 0, 1, 1, 0, 1, 0, 2]

    # Separate the names and the numeric data
    numeric_data = [entry[1:] for entry in data]

    # Convert the numeric data to a numpy array
    numeric_data = np.array(numeric_data)

    total_mrkt_cap = sum(entry[2] for entry in data)

    for entry in data:
    # Update 'np_qtr' normalising with market cap
        entry[4] = entry[4] / (100 * (entry[2] / total_mrkt_cap))

    for entry in data:
    # Update 'np_qtr' normalising with market cap
        entry[6] = entry[6] / (100 * (entry[2] / total_mrkt_cap))
   
    # Normalize the numeric data
    data_normalized = (numeric_data - np.min(numeric_data, axis=0)) / (np.max(numeric_data, axis=0) - np.min(numeric_data, axis=0)) 

    # Calculate the score for each stock
    scores = np.sum(data_normalized * preference, axis=1)

    #normalize
    softmax_scores = np.exp(scores) / np.sum(np.exp(scores), axis=0)

    # Combine the scores with the stock names
    data_scored = list(zip(np.array(data)[:, 0], softmax_scores))

    # Sort the stocks by score
    data_scored.sort(key=lambda x: x[1], reverse=True)

    return {"data": data,"preference":data_scored}