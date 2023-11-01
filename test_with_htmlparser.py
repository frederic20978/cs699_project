from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, MetaData, Column, String, Float, inspect
from sqlalchemy.sql import text

def main():
    with open('output.txt', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
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
    
    update_db(data)

def update_db(data):
    table_name = "computer_software"

    engine = create_engine('postgresql://fred:4004@localhost/699_project',isolation_level="AUTOCOMMIT")

    # conn = psycopg2.connect(
    #     dbname="699_project",
    #     user="fred",
    #     password="4004",
    #     host="localhost"
    # )

    # Initialize metadata
    metadata = MetaData()

    # Check if the table exists
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        # If the table exists, drop it
        engine.execute(f"DROP TABLE {table_name}")
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
            print(entry)
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

if __name__== "__main__":
    main()