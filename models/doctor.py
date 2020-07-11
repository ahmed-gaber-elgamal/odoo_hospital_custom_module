from odoo import models, fields, api, _
class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    # doctor_name=fields.Many2one('res.partner', string='Doctor', required=True)
    doctor_name=fields.Char(string='Doctor', required=True)
    doctor_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ], string='Gender', default='male')
    patient_id = fields.Many2one('hospital.patient', string='Related User', required=True)
    appointment_ids = fields.Many2many('hospital.appointment', string='Appointments')
    def name_get(self):
        result = []
        for doctor in self:
            name = doctor.doctor_name
            result.append((doctor.id, name))
        return result