from sqlalchemy import create_engine, Table, MetaData, Column, String, Float, inspect
from sqlalchemy.sql import text
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests

def update_db(data,table_name):
    #     dbname="699_project",
    #     user="fred",
    #     password="4004",
    #     host="localhost"
    engine = create_engine('postgresql://fred:4004@localhost/699_project',isolation_level="AUTOCOMMIT")
    
    # Initialize metadata
    metadata = MetaData()

    # Check if the table exists
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        # If the table exists, drop it
        with engine.connect() as connection:
            drop_table_sql = text(f"DROP TABLE IF EXISTS {table_name}")
            connection.execute(drop_table_sql)
        print(f"Table '{table_name}' has been dropped.")
    else:
        print(f"Table '{table_name}' does not exist.")

    # Create table
    table = Table(table_name, metadata,
                  Column('name', String),
            Column('cmp', Float),
            Column('pe', Float),
            Column('market_cap', Float),
            Column('div_yield', Float),
            Column('np_qtr', Float),
            Column('qtr_profit_var', Float),
            Column('sales', Float),
            Column('sales_var', Float),
            Column('roce', Float))
    metadata.create_all(engine)

    # Start a new session   
    with engine.connect() as connection:
        # Iterate over data entries
        for entry in data:
            # Build insert statement
            stmt = table.insert().values(
                name=entry['name'], 
                cmp=entry['cmp'], 
                pe=entry['pe'], 
                market_cap=entry['market_cap'], 
                div_yield=entry['div_yield'], 
                np_qtr=entry['np_qtr'], 
                qtr_profit_var=entry['qtr_profit_var'], 
                sales=entry['sales'], 
                sales_var=entry['sales_var'], 
                roce=entry['roce']
            )
            # Execute insert statement
            connection.execute(stmt)

def scrap_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr', attrs={'data-row-company-id': True})

    data = []
    # Loop over the rows
    for row in rows:
        # Find all 'td' elements in this row
        cols = row.find_all('td')
        
        # Extract the data
        content = { "name" : cols[1].text.strip(),
            "cmp" : float(cols[2].text.strip()),
            "pe" : float(cols[3].text.strip()),
            "market_cap" :float(cols[4].text.strip()),
            "div_yield" : float(cols[5].text.strip()),
            "np_qtr" : float(cols[6].text.strip()),
            "qtr_profit_var" : float(cols[7].text.strip()),
            "sales" : float(cols[8].text.strip()),
            "sales_var" : float(cols[9].text.strip()),
            "roce" : float(cols[10].text.strip()),
        }
        data.append(content)
    return data

def create_visuals(data,domain):
    name = [entry['name'] for entry in data]
    profits = [entry['np_qtr'] for entry in data]
    # Create a bar graph
    plt.bar(names, profits)

    plt.title('Net Profits of Companies')
    plt.xlabel('Company')
    plt.ylabel('Net Profit')

    # Display the graph
    plt.show()


def main():
    data = scrap_data("https://www.screener.in/company/compare/00000034/00000027/")
    update_db(data,"computer_software")
    create_visuals(data,"computer_software")
    
    data = scrap_data("https://www.screener.in/company/compare/00000057/00000084/")
    update_db(data,"steel")


if __name__== "__main__":
    main()