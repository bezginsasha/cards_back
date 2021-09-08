from pathlib import Path
from datetime import datetime
import re

from werkzeug.utils import secure_filename
from openpyxl import load_workbook


class WrongFileExtensionError(Exception):
    def __init__(self, message):
        self.message = message


def create_or_get_dir():
    import_dir = Path.cwd() / 'import'
    if not import_dir.exists():
        import_dir.mkdir()
    return import_dir


def create_file_name_with_date_and_username(file_name, username):
    match = re.match(r'(.+)\.xlsx$', file_name)
    file_name_without_extension = match.group(1)
    datetime_now = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    file_name = f'{file_name_without_extension}_{username}_{datetime_now}.xlsx'
    return file_name


def save_file(import_dir, file, username):
    file_name = secure_filename(file.filename)
    if file_name.endswith('.xlsx'):
        file_name = create_file_name_with_date_and_username(file_name, username)
        file.save(import_dir / file_name)
        return file_name
    else:
        raise WrongFileExtensionError('Wrong file extension, xlsx needed')


def iter_excel(import_dir, file_name):
    excel = load_workbook(import_dir / file_name)
    first_sheet = excel.worksheets[0]
    for row in first_sheet.values:
        yield row
