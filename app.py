import streamlit as st
import pandas as pd

# Example title
st.title("AI Agent Dashboard")
# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)  # Display the uploaded dataframe
