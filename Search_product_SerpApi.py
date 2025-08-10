import requests
import os

# Your API key
API_KEY = os.environ.get("SERPAPI_API_KEY")

# Search query
query = "iPhone 15 Pro Max"

# SerpApi endpoint
url = "https://serpapi.com/search.json"

# Parameters
params = {
    "engine": "google_shopping",
    "q": query,
    "api_key": API_KEY
}

# Make the request
response = requests.get(url, params=params)

# Check status and print JSON
if response.status_code == 200:
    data = response.json()
    print(data)  # raw JSON output
else:
    print(f"Error: {response.status_code}")
