from dotenv import load_dotenv
load_dotenv()
import requests
import time
import os
import csv
import json

api_key = os.getenv("polygon_api_key")

url = f'https://api.polygon.io/v3/reference/tickers?market=indices&active=true&order=asc&limit=100&sort=ticker&apiKey={api_key}'

response = requests.get(url)
data = response.json()
tickers = []

if 'results' in data:
    for ticker in data['results']:
        tickers.append(ticker)
else:
    print("'results' key not found in API response. Full response:")
    print(json.dumps(data, indent=2))
api_calls = 1
while 'next_url' in data:
    print('Requesting next page')
    response = requests.get(data['next_url'] + f'&apiKey={api_key}')
    api_calls += 1
    print(f'api calls: {api_calls}')
    if api_calls >= 4:
        print("Reached API call limit for this session.")
        time.sleep(60)
        api_calls = 0
    data = response.json()
    if 'results' in data:
        for ticker in data['results']:
            tickers.append(ticker)
    else:
        print("'results' key not found in API response. Full response:")
        print(json.dumps(data, indent=2))
        break

    

# Write to CSV file using ticker keys as headers
if tickers:
    with open('index_tickers.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=tickers[0].keys())
        writer.writeheader()
        writer.writerows(tickers)

    
    
    