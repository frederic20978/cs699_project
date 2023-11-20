from fastapi import FastAPI
import numpy as np
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware



def analyse_data(data):
    # prefernce list
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

    for i, entry in enumerate(data):
        entry.append(round(softmax_scores[i]*100,2))

    # Sort the stocks by score
    data.sort(key=lambda x: x[-1], reverse=True)

    return {"data": data,"preference":data_scored}


# Replace these values with your actual database connection details
def fetch_data(table_name):
    engine = create_engine('postgresql://naveen:473089@localhost/db',isolation_level="AUTOCOMMIT")

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
    return data

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origin of your frontend in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get_data/computer_software")
def get_data_computer_software():
    #Calling function to fetch data form database
    data = fetch_data("computer_software")
    # function to analyse the stock
    result  = analyse_data(data)
    # return data in json format
    return result

@app.get("/get_data/steel")
def get_data_steel():
    #Calling function to fetch data form database
    data = fetch_data("steel")
    # function to analyse the stock
    result  = analyse_data(data)
    # return data in json format
    return result

@app.get('/get_data/fmcg')
def get_data_fmcg():
    # Calling function to fetch data from the database for fmcg
    data = fetch_data('fmcg')
    # Function to analyze the stock for fmcg
    result = analyse_data(data)
    # Return data in JSON format
    return result