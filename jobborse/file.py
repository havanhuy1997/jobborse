import pyexcel
from django.conf import settings
import os

class Excel:
    def __init__(self, file_name):
        self.file_name = os.path.join(settings.BASE_DIR + '/' + settings.MEDIA_ROOT, file_name)
        print(self.file_name)
        self.sheet = pyexcel.get_sheet(file_name=self.file_name)

    def get_lines(self):
        f = open(self.file_name, 'rb')
        return pyexcel.get_records(file_type='xlsx', file_content=f.read())

    def add_row(self, row):
        self.sheet.row += row

    def save(self):
        self.sheet.save_as(self.file_name)