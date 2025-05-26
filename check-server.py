import os
import platform
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configura tu IP o dominio
SERVER = "168.176.123.121"

# Define el número de pings que se realizarán
PING_COUNT = 5

# Configura las credenciales de Google Sheets
SPREADSHEET_NAME = "historico"
WORKSHEET_NAME = "historico"
JSON_CREDENTIALS_FILE = "credentials.json"  # Tu archivo de credenciales

def ping_server(server, count=4):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} {count} {server}"
    response = os.popen(command).read()
    
    if "0% loss" in response or "0% perdidos" in response:
        return "Funcionando"
    elif "100% loss" in response or "100% perdidos" in response:
        return "Caído"
    else:
        return "Intermitente"

def log_to_spreadsheet(state):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)

    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

    # Obtener hora actual en UTC-5 (restando 5 horas a UTC)
    timestamp = (datetime.datetime.utcnow() - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Agregar fila al sheet
    sheet.append_row([timestamp, SERVER, state])

if __name__ == "__main__":
    status = ping_server(SERVER, PING_COUNT)
    log_to_spreadsheet(status)
