from django import forms
from django.shortcuts import HttpResponse
import xlwt


class ExportBaseForm(forms.Form):

    HEADERS, SHEET_NAME = [], "sheet1"
    FILE_NAME = "export"

    def __init__(self, *args, **kwargs):
        super(ExportBaseForm, self).__init__(*args, **kwargs)
        self.object_list, self.response = [], HttpResponse(content_type='application/ms-excel')
        self.response['Content-Disposition'] = 'attachment; filename="%s.xls"' % self.FILE_NAME
        self.work_book, self.work_sheet = xlwt.Workbook(encoding="utf-8"), None
        self.work_sheet = self.work_book.add_sheet(self.SHEET_NAME)
        self.row = 0

    def generate_title(self):
        pass

    def generate_header(self):
        self.update_header()
        for index, header in enumerate(self.HEADERS):
            self.work_sheet.write(self.row, index, header)
        self.row_increment()

    def update_header(self):
        return self.HEADERS

    def generate_body(self):
        raise ValueError("Must implement body")

    def export_template(self):
        self.generate_title()
        self.generate_header()
        self.generate_body()

        self.update_file_name()

        self.work_book.save(self.response)
        return self.response

    def row_increment(self, steps=1):
        self.row += steps

    def update_file_name(self):
        self.response['Content-Disposition'] = 'attachment; filename="{0}.xls"'.format(self.FILE_NAME)