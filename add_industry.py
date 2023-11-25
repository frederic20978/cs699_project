from bs4 import BeautifulSoup
import ast

def modify_html():
    # Read the HTML file
    with open('./static/mypage.html', 'r') as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a new button element
    new_button = soup.new_tag('button', id='nav_fmcg', onclick="fetchData('http://localhost:8000/get_data/fmcg', 'fmcg')")
    new_button.string = 'FMCG'

    # Find the top-bar div and append the new button
    top_bar_div = soup.find('div', class_='top-bar')
    top_bar_div.append(new_button)

    # Save the modified HTML content
    with open('modified_html_file.html', 'w') as file:
        file.write(str(soup))

def modify_fastApi():
    industry = "fmcg"
    with open("apis.py", "a") as file:
        endpoint = f"/get_data/{industry}"
        file.write("\n")
        file.write(f"@app.get('{endpoint}')\n")
        file.write(f"def get_data_{industry}():\n")
        file.write(f"    # Calling function to fetch data from the database for {industry}\n")
        file.write(f"    data = fetch_data('{industry}')\n")
        file.write(f"    # Function to analyze the stock for {industry}\n")
        file.write(f"    result = analyse_data(data)\n")
        file.write("    # Return data in JSON format\n")
        file.write("    return result\n")

    print("Code has been written to routes.py")

if __name__ =="__main__":
    modify_html()
    modify_fastApi()