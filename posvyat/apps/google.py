import logging
from gspread import Client, Spreadsheet, service_account, exceptions
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .models import Registration, Transfer, Rasselenie

# ID Google таблицы
TABLE_ID = '1_jxyRGncretB5OAtRyOZVgoO00WSXQXnGQcm8CoCv8Y'


def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    try:
        return service_account(filename='myapp/posvyat-2bba2418def2.json')
    except exceptions.GSpreadException as e:
        logging.error("Ошибка при создании клиента: %s", e)
        return None


def get_table_by_id(client: Client, table_id: str) -> Spreadsheet:
    """Получение таблицы из Google Sheets по ID таблицы."""
    try:
        return client.open_by_key(table_id)
    except exceptions.GSpreadException as e:
        logging.error("Ошибка при получении таблицы: %s", e)
        return None


def get_all_sheets(spreadsheet: Spreadsheet) -> list:
    """Возвращает все листы из Google таблицы."""
    try:
        return spreadsheet.worksheets()
    except exceptions.GSpreadException as e:
        logging.error("Ошибка при получении листов: %s", e)
        return []


def upload_registration_data(client: Client) -> None:
    """Выгрузка данных в гугл таблицу по регистрации"""
    spreadsheet = get_table_by_id(client, TABLE_ID)
    if spreadsheet is not None:
        worksheet = spreadsheet.sheet1  # первый лист будет чисто для регистрации
        registration_data = list(Registration.objects.all())
        worksheet.insert_rows(registration_data, 2)


def upload_transfer_data(client: Client) -> None:
    """Выгрузка данных в гугл таблицу по трансферам"""
    spreadsheet = get_table_by_id(client, TABLE_ID)
    if spreadsheet is not None:
        worksheet = spreadsheet.get_worksheet(1)  # второй лист для трансферов
        transfer_data = list(Transfer.objects.all())
        worksheet.insert_rows(transfer_data, 2)


def upload_rasselenie_data(client: Client) -> None:
    """Выгрузка данных в гугл таблицу по расселению"""
    spreadsheet = get_table_by_id(client, TABLE_ID)
    if spreadsheet is not None:
        worksheet = spreadsheet.get_worksheet(2)  # третий лист для расселения
        rasselenie_data = list(Rasselenie.objects.all())
        worksheet.insert_rows(rasselenie_data, 2)


def background_update():
    """Функция для планирования обновления таблиц в фоне."""
    client = client_init_json()
    if client is not None:
        upload_registration_data(client)
        upload_transfer_data(client)
        upload_rasselenie_data(client)


def start_scheduler():
    """Запуск планировщика для обновления таблиц в фоне."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(background_update, 'interval', minutes=1)
    scheduler.start()
