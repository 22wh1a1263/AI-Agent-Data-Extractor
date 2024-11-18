# utils/web_search.py
import requests

def search_web(query):
    # Use an API or a method for web search, such as scraping or using a search engine API
    return requests.get(f"https://api.searchengine.com?q={query}").json()
