import os
import logging
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load Google Sheets API Credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# ID Google Sheets dari environment variable
SPREADSHEET_ID = os.getenv("SHEET_ID")
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Fungsi untuk mengambil data berdasarkan ID
def get_data(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text("Gunakan format: /get <ID>")
            return
        
        row_id = context.args[0]
        data = sheet.get_all_records()
        
        for row in data:
            if str(row["ID"]) == row_id:
                response = f"Nama: {row['Nama']}\nUmur: {row['Umur']}\nKota: {row['Kota']}"
                update.message.reply_text(response)
                return
        
        update.message.reply_text("Data tidak ditemukan.")

    except Exception as e:
        logging.error(f"Error: {e}")
        update.message.reply_text("Terjadi kesalahan.")

# Fungsi utama untuk menjalankan bot
def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("get", get_data))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
