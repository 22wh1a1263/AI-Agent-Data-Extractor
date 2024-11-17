import streamlit as st
import pandas as pd
import requests
import json
from openai import ChatCompletion
import os

# Set up Streamlit page configuration
st.set_page_config(page_title="AI Agent Data Extractor", layout="wide")

# Title and description
st.title("AI Agent Data Extractor")
st.write("Upload your data, perform searches, and extract insights with GPT-powered AI!")

# Step 1: File Upload
st.subheader("1. Upload CSV or Connect Google Sheets")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Google Sheets input (Optional)
sheet_url = st.text_input("Enter Google Sheets URL (optional)")
data = None

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

elif sheet_url:
    # Fetch data from Google Sheets
    st.write("Fetching data from Google Sheets...")
    try:
        # Extract Google Sheets ID
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        data = pd.read_csv(url)
        st.write("Data Preview:", data.head())
    except Exception as e:
        st.error("Failed to load data from Google Sheets. Ensure the URL is correct and the sheet is public.")

# Step 2: Select Column for Entities
if data is not None:
    st.subheader("2. Select Entity Column")
    entity_column = st.selectbox("Select the column containing entities (e.g., company names):", data.columns)

    # Step 3: Enter Query Template
    st.subheader("3. Enter Query Template")
    query_template = st.text_area(
        "Enter your query template. Use {entity} as a placeholder.",
        value="Find the email address of {entity}.",
    )

    # Process button
    if st.button("Run AI Agent"):
        if entity_column and query_template:
            st.write("Processing your request...")
            results = []

            # Iterate over each entity in the selected column
            for entity in data[entity_column].dropna():
                # Replace placeholder with the actual entity
                query = query_template.replace("{entity}", entity)
                st.write(f"Query for {entity}: {query}")

                # Step 4: Web Search (Placeholder)
                # Use SerpAPI or similar service here
                # For now, we'll just simulate search results
                simulated_search_results = {
                    "urls": [f"http://example.com/{entity}"],
                    "snippets": [f"Simulated result for {entity}"],
                }

                # Step 5: GPT Processing
                openai_api_key = st.secrets["OPENAI_API_KEY"]
                if openai_api_key:
                    # Initialize OpenAI API client
                    ChatCompletion.api_key = openai_api_key
                    response = ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Extract the email from the following text."},
                            {"role": "user", "content": f"Text: {simulated_search_results['snippets'][0]}"},
                        ],
                    )
                    extracted_info = response.choices[0].message["content"]
                else:
                    extracted_info = "No API key found!"

                # Save results
                results.append({"Entity": entity, "Extracted Info": extracted_info})

            # Step 6: Display Results
            st.subheader("4. Extracted Results")
            result_df = pd.DataFrame(results)
            st.write(result_df)

            # Download CSV
            st.download_button(
                label="Download Results as CSV",
                data=result_df.to_csv(index=False),
                file_name="results.csv",
                mime="text/csv",
            )
else:
    st.info("Upload a CSV file or provide a Google Sheets URL to start.")

# Footer
st.markdown("Created by Neha. Powered by Streamlit, OpenAI GPT, and SerpAPI.")

