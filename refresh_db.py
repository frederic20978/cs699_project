import psycopg2
from psycopg2.extensions import AsIs
from bs4 import BeautifulSoup
import requests

def update_db(data,sector):
    conn = psycopg2.connect(
        dbname="699_project",
        user="fred",
        password="4004",
        host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS %s",(AsIs(sector),))
    conn.commit()

    # Create table columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS %s (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        cmp FLOAT,
        pe FLOAT,
        market_cap FLOAT,
        div_yield FLOAT,
        np_qtr FLOAT,
        qtr_profit_var FLOAT,
        sales FLOAT,
        sales_var FLOAT,
        roce FLOAT
    )
    """,(AsIs(sector),))
    conn.commit()

    # Insert new data
    for entry in data:
        cursor.execute("""
        INSERT INTO stock_data (name, cmp, pe, market_cap, div_yield, np_qtr, qtr_profit_var, sales, sales_var, roce) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (entry['name'], entry['cmp'], entry['pe'], entry['market_cap'], entry['div_yield'], entry['np_qtr'], entry['qtr_profit_var'], entry['sales'], entry['sales_var'], entry['roce']))
    conn.commit()

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

def main():
    data = scrap_data("https://www.screener.in/company/compare/00000034/00000027/")
    update_db(data,"computer_software")

if __name__== "__main__":
    main()