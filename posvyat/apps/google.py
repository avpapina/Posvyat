from gspread import Client, Spreadsheet, Worksheet, service_account, exceptions

table_id = '1_jxyRGncretB5OAtRyOZVgoO00WSXQXnGQcm8CoCv8Y'

def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename='myapp\posvyat-2bba2418def2.json')

def get_table_by_id(client: Client, table_id):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_id)
