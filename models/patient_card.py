from odoo import models, fields, api, _
class PatientCardReport(models.AbstractModel):
    _name = 'report.hospital.report_patient'
    _description = 'Patient Card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('i am here')
        print('docids', docids)
        docs = self.env['hospital.patient'].browse(docids[0])
        appointments=self.env['hospital.appointment'].search([('patient_id','=',docids[0])])
        appointment_list=[]
        for app in appointments:
            vals={
                'name':app.name,
                'notes':app.notes,
                'appointment_date':app.appointment_date
            }
            appointment_list.append(vals)
        print('appointments',appointments)
        print('appointment_list', appointment_list)
        return {
            'doc_model': 'hospital.patient',
            'data': data,
            'docs': docs,
            "appointment_list":appointment_list
        }