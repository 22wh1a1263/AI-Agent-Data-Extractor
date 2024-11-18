# utils/sheets_api.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def fetch_google_sheet(sheet_url):
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)
    return pd.DataFrame(worksheet.get_all_records())

def write_to_sheet(sheet_url, data):
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())
