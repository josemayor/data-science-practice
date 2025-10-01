# run by: python tesla.py
# This code extracts stock data for Tesla and GameStop using yfinance and web scraping, then
# visualizes the stock prices and revenues using Plotly.

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
# from bs4 import XMLParsedAsHTMLWarning
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    # fig.show()
    fig.write_html("grafico.html", auto_open=True)

    # If you are running this code in a Jupyter notebook, uncomment the following lines to display the plot inline
    # -------------------------------
    #from IPython.display import display, HTML
    #fig_html = fig.to_html()
    #display(HTML(fig_html))
    # -------------------------------





"""
QUESTION 1: Use yfinance to Extract Stock Data
----------------------------------------------

Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object.
The stock is Tesla and its ticker symbol is `TSLA`.
"""

tesla = yf.Ticker("TSLA")
tesla_info = tesla.info
tesla_history = tesla.history(period="max")

tesla_price = tesla.info['currentPrice']
print(f"Tesla Current Price: {tesla_price}")

reset_index = tesla_history.reset_index(inplace=True)
# Display the first five rows of the tesla_history dataframe
print(tesla_history.head())
# reset_index['Date'] = reset_index['Date'].astype(str)

# halt the execution to see the output
pause = input("Press Enter to continue...")



"""
QUESTION 2: Use Webscraping to Extract Tesla Revenue Data
---------------------------------------------------------

Use the requests library to download the webpage
https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm
Save the text of the response as a variable named html_data.
"""

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
data = requests.get(url)
soup = BeautifulSoup(data.content, 'html.parser')

print (soup.title)
print("-----------------------------------")

# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Revenue` and store it into a dataframe named `tesla_revenue`.
# The dataframe should have columns `Date` and `Revenue`.

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
table = soup.find('table')
rows = table.find_all('tr')
for row in rows[1:]:
    cols = row.find_all('td')
    date = cols[0].text.strip()
    revenue = cols[1].text.strip()
    tesla_revenue = tesla_revenue._append({"Date": date, "Revenue": revenue}, ignore_index=True)


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print(tesla_revenue.tail())



"""
QUESTION 3: Use yfinance to Extract Stock Data
----------------------------------------------

Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object.
The stock is GameStop and its ticker symbol is `GME`.
Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`.
Set the `period` parameter to ` "max" ` so we get information for the maximum amount of time.

Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of
the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of
Question 3 to the results below.
"""

print("---")
gamestop = yf.Ticker("GME")
gamestop_info = gamestop.info
gme_data = gamestop.history(period="max")

gamestop_price = gamestop.info['currentPrice']
print(f"GameStop Current Price: {gamestop_price}")

reset_index = gme_data.reset_index(inplace=True)
# Display the first five rows of the gme_data dataframe
print(gme_data.head())



"""
QUESTION 4: Use Webscraping to Extract GME Revenue Data
---------------------------------------------------------
Use the requests library to download the webpage
https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/gme_revenue.htm
Save the text of the response as a variable named html_data.
"""

print("---")
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
data = requests.get(url)
html_data = data.text
soup = BeautifulSoup(data.content, 'html.parser')
print (soup.title)
print("-----------------------------------")
# Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Revenue` and store it into a dataframe named `gme_revenue`.
# The dataframe should have columns `Date` and `Revenue`.
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
table = soup.find('table')
rows = table.find_all('tr')
for row in rows[1:]:
    cols = row.find_all('td')
    date = cols[0].text.strip()
    revenue = cols[1].text.strip()
    gme_revenue = gme_revenue._append({"Date": date, "Revenue": revenue}, ignore_index=True)   

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
print(gme_revenue.tail())


"""
QUESTION 5: Plot Tesla Stock Graph
-----------------------------
Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. Note the graph will only show data upto June 2021.
You just need to invoke the make_graph function with the required parameter to print the graphs.The structure to call the `make_graph` function is 
"make_graph(tesla_data, tesla_revenue, 'Tesla')".
"""

make_graph(tesla_history, tesla_revenue, 'Tesla')


"""
Question 6: Plot GameStop Stock Graph

Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the make_graph
function is make_graph(gme_data, gme_revenue, 'GameStop'). Note the graph will only show data upto June 2021.
"""

make_graph(gme_data, gme_revenue, 'GameStop')
