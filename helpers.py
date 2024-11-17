import streamlit as st
import pandas as pd
import requests

# Function to upload CSV file
def upload_csv():
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

# Function to query entities using SerpAPI
def query_entities(entity, query_template, serpapi_key):
    search_query = query_template.format(entity=entity)
    params = {
        "q": search_query,
        "api_key": serpapi_key,
    }
    search_url = "https://serpapi.com/search"
    response = requests.get(search_url, params=params)
    results = response.json()
    return results.get("organic_results", [])

# Function to display results in a Streamlit table
def display_results(results):
    if results:
        st.write("### Extracted Data")
        df = pd.DataFrame(results)
        st.write(df)
    else:
        st.write("No data found.")
