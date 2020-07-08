# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class SaleOrderInherit(models.Model):
    _inherit='sale.order'
    patient_name=fields.Char(string=' Patient Name')
    def action_confirm(self):
        print('inherited successufully')
        res=super(SaleOrderInherit, self).action_confirm()
        return res
class ResPartner(models.Model):
    _inherit='res.partner'
    company_type=fields.Selection(selection_add=[('iti', 'iti')])
    @api.model
    def create(self, vals_list):
        res=super(ResPartner, self).create(vals_list)
        print("it's working...")
        return res

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'patient record'
    _inherit=['mail.thread', 'mail.activity.mixin']

    def action_patients(self):
        print('oooooooooooooo')
        return {
            'name': _('patient server action'),
            'view_mode': 'tree,form',
            'res_model': 'hospital.patient',
            'domain': [],
            'view_id': False,
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            }
    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age<5:
                raise ValidationError(_("Age must be greater than 5"))

    @api.model
    def test_cron_job(self):
        print('test cron job')
    def open_patient_appointment(self):
        return {
            'name': _('Appointment'),
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'domain':[('patient_id','=',self.id)],
            'view_id': False,
            'view_type': 'form',
            # 'target': 'new',
            # 'views': False,
            'type': 'ir.actions.act_window',
            # 'context': self.env.context,
        }

    @api.depends('age')
    def set_age_group(self):
        for rec in self:

            if rec.age:
                if rec.age<18:
                    rec.age_group='minor'
                else:
                    rec.age_group='major'

    def count_appointment(self):
        count=self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count=count
    @api.onchange('doctor_name')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_name:
                rec.doctor_gender=rec.doctor_name.doctor_gender

    def name_get(self):
        result = []

        for record in self:
            result.append((record.id, "%s%s" % (record.name_seq, record.name)))
        return result

    def action_send_email(self):
        template_id=self.env.ref('hospital.patient_card_email_template').id
        template=self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
    def print_report(self):
        return self.env.ref('hospital.patient_report').report_action(self)
    def print_report_excel(self):
        return self.env.ref('hospital.patient_report_xlx').report_action(self)

    name=fields.Char(string='Name', required=True)
    age=fields.Integer(string='Age', track_visibility='always', group_operator=False)
    age2 = fields.Float(string='Age2')
    notes=fields.Text(string='Notes')
    image=fields.Binary(string='Image', attachment=True)
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,  index=True, default=lambda self: _('New'))
    gender = fields.Selection([ ('male', 'Male'),('female', 'Female'),],string='Gender', default='male')
    age_group=fields.Selection([ ('major', 'Major'),('minor', 'Minor'),],string='Age Group', compute='set_age_group', store=True)
    appointment_count=fields.Integer(string='Appointment Count', compute='count_appointment')
    active = fields.Boolean('Active', default=True)
    doctor_name=fields.Many2one('hospital.doctor', string='Doctor')
    doctor_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ], string=' Doctor Gender')
    patient_email=fields.Text(string='email')
    user_id=fields.Many2one('hospital.patient', string='PRO')
    patient_name_upper=fields.Char(compute='_compoute_upper_name', inverse='_inverse_upper_name')

    @api.depends('name')
    def _compoute_upper_name(self):
        for rec in self:
            rec.patient_name_upper=rec.name.upper() if rec.name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.name = rec.patient_name_upper.lower() if rec.patient_name_upper else False


    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result=super(HospitalPatient, self).create(vals)
        return result