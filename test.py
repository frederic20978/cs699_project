from bs4 import BeautifulSoup
import requests

def main():
    url = "https://www.screener.in/company/compare/00000034/00000027/"
    response = requests.get(url)
    html_content = response.text
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    
if __name__== "__main__":
    main()