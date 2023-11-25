from sqlalchemy import create_engine, Table, MetaData, Column, String, Float, inspect
from sqlalchemy.sql import text
from configparser import ConfigParser
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests

def update_db(data,table_name):
    # Read the configuration file
    config = ConfigParser()
    config.read('config.ini')

    # Get the database connection details
    username = config['database']['username']
    password = config['database']['password']
    host = config['database']['host']
    database_name = config['database']['database_name']

    # Create the database connection string
    connection_string = f'postgresql://{username}:{password}@{host}/{database_name}'
    
    # Create the SQLAlchemy engine
    engine = create_engine(connection_string, isolation_level="AUTOCOMMIT")
    
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

def create_visuals(data,domain="computer_software"):
    name = [entry['name'] for entry in data]
    total_mrkt_cap = sum(entry['market_cap'] for entry in data)

    #for profits
    profits = [entry['np_qtr']/(100*(entry['market_cap']/total_mrkt_cap)) for entry in data]

    # Create a bar graph
    plt.bar(name, profits)
    plt.title('Market Cap-Weighted Net Profit')
    plt.xlabel('Company')
    plt.ylabel('Net Profit')

    # Rotate x-axis labels
    plt.xticks(rotation=90)

    # Adjust bottom margin
    plt.gcf().subplots_adjust(bottom=0.35)

    # Save the graph
    plt.savefig(f'static/images/{domain}_net_profits.png')
    plt.clf()

    #for p/e ratio
    pe = [entry['pe'] for entry in data]

    # Create a bar graph
    plt.plot(name, pe, marker='o', linestyle='-')
    plt.title('P/E ratio of Companies')
    plt.xlabel('Company')
    plt.ylabel('P/E')

    # Rotate x-axis labels
    plt.xticks(rotation=90)

    # Adjust bottom margin
    plt.gcf().subplots_adjust(bottom=0.35)

    # Save the graph
    plt.savefig(f'static/images/{domain}_pe.png')
    plt.clf()

    #for sales ratio
    sales = [entry['sales']/(100*(entry['market_cap']/total_mrkt_cap)) for entry in data]

    # Create a bar graph
    plt.bar(name, sales)
    plt.title('Sales of Companies Normalized')
    plt.xlabel('Company')
    plt.ylabel('Sales')

    # Rotate x-axis labels
    plt.xticks(rotation=90)

    # Adjust bottom margin
    plt.gcf().subplots_adjust(bottom=0.35)

    # Save the graph
    plt.savefig(f'static/images/{domain}_sales.png')
    plt.clf()

    #for market_cap
    market_cap = [entry['market_cap'] for entry in data]

    # Create a pie chart
    plt.pie(market_cap, labels=name, autopct='%1.1f%%')
    plt.gcf().subplots_adjust(bottom=0)
    plt.title('Market Capitalization of Companies')

    # Save the graph
    plt.savefig(f'static/images/{domain}_market_cap.png')
    plt.clf()


def main():
    data = scrap_data("https://www.screener.in/company/compare/00000034/00000027/")
    update_db(data,"computer_software")
    create_visuals(data,"computer_software")
    
    data = scrap_data("https://www.screener.in/company/compare/00000057/00000084/")
    update_db(data,"steel")
    create_visuals(data,"steel")

    data = scrap_data("https://www.screener.in/company/compare/00000027/")
    update_db(data,"fmcg")
    create_visuals(data,"fmcg")

    # data = scrap_data("https://www.screener.in/company/compare/00000006/00000011/")
    # update_db(data,"bank")
    # create_visuals(data,"bank")

if __name__== "__main__":
    main()