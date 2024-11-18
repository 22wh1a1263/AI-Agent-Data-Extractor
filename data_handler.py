# utils/data_handler.py
import pandas as pd

def process_uploaded_file(uploaded_file):
    return pd.read_csv(uploaded_file)
