import psycopg2
from bs4 import BeautifulSoup
import requests

def refresh_data(data):
    conn = psycopg2.connect(
        dbname="699_project",
        user="fred",
        password="4004",
        host="localhost"
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM stock_data")
    conn.commit()
    # create table columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        value VARCHAR(255)
    )
    """)
    conn.commit()

    for entry in data:
        cursor.execute("INSERT INTO stock_data (name, value) VALUES (%s, %s)", (entry['name'], entry['value']))
    conn.commit()

def main():
    url = "https://www.ndtv.com/business/marketdata/stocks-gainers/nifty_monthly"
    response = requests.get(url)
    html_content = response.text
    # soup = BeautifulSoup(html_content, 'html.parser')
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')
    green_btn_elements = soup.find_all(class_="green-btn")

    # Extract the names of the stocks and numbers
    stocks= []

    for element in green_btn_elements:
        stock_name = element.find_previous("a").get_text()
        number = element.get_text()
        stocks.append({"name":stock_name,"value":number})
    
    stocks = list(filter(lambda x: x["value"].count("%")==1,stocks))
    refresh_data(stocks)

main()