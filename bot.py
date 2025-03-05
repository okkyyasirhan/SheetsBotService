import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("config.json")
client = gspread.authorize(creds)
