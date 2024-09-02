import logging

import gspread
from gspread import Client, Spreadsheet, service_account, exceptions, GSpreadException
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .models import Registration, Transfer, Rasselenie

# ID Google таблицы
# TABLE_ID = '1_jxyRGncretB5OAtRyOZVgoO00WSXQXnGQcm8CoCv8Y' # основной посвятовский
TABLE_ID = '1LV6v5lu5F5rgiRgXoVHss-lxwjbtInOhfDhgiACCKQI'  # моё для тестов УБРАТЬ в финалке


def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    try:
        return service_account(filename='app/dhsjowpld-6c713a315b3f.json') # filename для тестов ПОМЕНЯТЬ НА НУЖНОЕ в финалке
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


def create_sheets(client: Client, table_id: str) -> None:
    spreadsheet = client.open_by_key(table_id)
    try:
        spreadsheet.worksheet('Registration')
        spreadsheet.worksheet('Transfer')
        spreadsheet.worksheet('Rasselenie')
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title='Registration', rows=100, cols=20)
        worksheet.insert_row([
            "Name", "Surname", "Middle Name", "VK", "TG", "Phone", "Birthday", "Sex",
            "University", "Faculty", "Group", "Transfer", "Course", "Health Features"
        ], 1)
        worksheet = spreadsheet.add_worksheet(title='Transfer', rows=100, cols=20)
        worksheet.insert_row(["Name", "Surname", "Middle Name", "Email", "VK", "TG", "Phone",
                              "From", "Departure Time"], 1)
        worksheet = spreadsheet.add_worksheet(title='Rasselenie', rows=100, cols=20)
        worksheet.insert_row(["Name", "Surname", "Middle Name", "VK", "TG", "Phone",
                              "Program", "Group", "Course", "People Custom"], 1)


def delete_data_from_sheets(client: Client) -> None:
    spreadsheet = get_table_by_id(client, TABLE_ID)
    sheets = spreadsheet.worksheets()
    
    for sheet in sheets:
        if sheet.title in ["Registration", "Transfer", "Rasselenie"]:
            range_to_clear = f"A2:{chr(64 + sheet.col_count)}{sheet.row_count}"
            sheet.batch_clear([range_to_clear])





def upload_registration_data(client: Client) -> None:
    """Выгрузка данных в гугл таблицу по регистрации"""
    spreadsheet = get_table_by_id(client, TABLE_ID)
    if spreadsheet is not None:
        worksheet = spreadsheet.worksheet('Registration')  # первый лист будет чисто для регистрации
        data_to_upload = []
        for registration in Registration.objects.all():
            row_data = [
                registration.name,
                registration.surname,
                registration.middle_name,
                registration.vk,
                registration.tg,
                str(registration.phone),
                registration.bday.strftime('%Y-%m-%d'),
                registration.sex,
                registration.university,
                registration.faculty,
                registration.group,
                registration.transfer,
                registration.course,
                registration.health_features
            ]
            data_to_upload.append(row_data)
        worksheet.insert_rows(data_to_upload, 2)


def upload_transfer_data(client: Client) -> None:
    """Выгрузка данных в гугл таблицу по трансферам"""
    spreadsheet = get_table_by_id(client, TABLE_ID)
    if spreadsheet is not None:
        worksheet = spreadsheet.worksheet('Transfer') # второй лист для трансферов
        data_to_upload = []
        for transfer_data in Transfer.objects.all():
            row_data = [
                transfer_data.name,
                transfer_data.surname,
                transfer_data.middle_name,
                transfer_data.email,
                transfer_data.vk,
                transfer_data.tg,
                str(transfer_data.phone),
                transfer_data._from,
                transfer_data.departure_time
            ]
            data_to_upload.append(row_data)
        worksheet.insert_rows(data_to_upload, 2)


def upload_rasselenie_data(client: Client) -> None:
    """Выгрузка данных в гугл таблицу по расселению"""
    spreadsheet = get_table_by_id(client, TABLE_ID)
    if spreadsheet is not None:
        worksheet = spreadsheet.worksheet('Rasselenie')  # третий лист для расселения
        data_to_upload = []
        for rasselenie_data in Rasselenie.objects.all():
            row_data = [
                rasselenie_data.name,
                rasselenie_data.surname,
                rasselenie_data.middle_name,
                rasselenie_data.vk,
                rasselenie_data.tg,
                str(rasselenie_data.phone),
                rasselenie_data.program,
                rasselenie_data.group,
                rasselenie_data.course,
                ', '.join(map(str, rasselenie_data.people_custom))
            ]
            data_to_upload.append(row_data)
        worksheet.insert_rows(data_to_upload, 2)


def background_update():
    """Функция для планирования обновления таблиц в фоне."""
    client = client_init_json()
    if client is not None:
        create_sheets(client, TABLE_ID)
        delete_data_from_sheets(client)
        upload_registration_data(client)
        upload_transfer_data(client)
        upload_rasselenie_data(client)


def start_scheduler():
    """Запуск планировщика для обновления таблиц в фоне."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(background_update, 'interval', minutes=1)
    scheduler.start()
