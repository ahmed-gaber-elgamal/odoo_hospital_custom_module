from odoo import models

class PatientCardXlsx(models.AbstractModel):
    _name = 'report.hospital.report_patient_xlx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print('lines', lines, data)
        format1=workbook.add_format({'font_size':14,'align':'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 14, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('patient card')
        # sheet.right_to_left()
        sheet.set_column(3,3,50)
        sheet.write(2 ,2, 'Name', format1)
        sheet.write(2, 3, lines.name, format2)
        sheet.write(3, 2, 'Age', format1)
        sheet.write(3, 3, lines.age, format2)