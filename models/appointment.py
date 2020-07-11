from odoo import models, fields, api, _
import pytz
import datetime
class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'patient_age desc'


    def test_recordset(self):
        for rec in self:
            partners=self.env['res.partner'].search([])
            print('partners................',partners.mapped('name'))
            print('partners................', partners.sorted(lambda g: g.create_date, reverse=True))
            print('partners................', partners.filtered(lambda g: g.user_id))

    def delete_lines(self):
        for rec in self:
            print('time in utc', rec.appointment_datetime)
            user_tz=pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            print(user_tz)
            date_today=pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            print('local time ..', date_today)
            rec.appointment_lines=[(5,0,0)]

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    
    

    def set_default_value(self):
        return "write your notes here!!"

    def confirm_state(self):
        for rec in self:
            rec.state='confirm'
        return {
            'effect': {
                'fadeout': 'slow',
                'message':'appointment confirmed',
                'type': 'rainbow_man',
            }
        }
    def done_state(self):
        for rec in self:
            rec.state='done'
    
    def write(self, vals):
        res=super(HospitalAppointment, self).write(vals)
        print('overwrite write function successfully')
        return res
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            # return {'domain':{'order_id':[('partner_id', '=',rec.partner_id.id)]}}
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        appointment_lines=[]
        product_rec=self.env['product.product'].search([])
        for pro in product_rec:
            line = (0,0,{
                'product_id':pro.id,
                'product_quantity':1
            })
            appointment_lines.append(line)
            res.update({
                "appointment_lines":appointment_lines,
                "patient_id":30,
                "notes":'odoo custom module...'
            })
        return res


    name=fields.Char(string='Appointment Id', required=True, copy=False, readonly=True, index=True,
                     default=lambda self:_('New'))
    patient_id=fields.Many2one('hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_age=fields.Integer('Age', related='patient_id.age')
    notes=fields.Text('Registeration Note', default=set_default_value)
    doctor_notes = fields.Text('Note')
    pharmacy_notes = fields.Text('Note')
    appointment_date=fields.Date(string='Start Date')
    appointment_end_date = fields.Date(string='End Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    state = fields.Selection([
        ('draft', 'draft'),
        ('confirm', 'confirm'),
        ('done', 'done')
    ], default="draft", string="Status")
    appointment_lines=fields.One2many('hospital.appointment.lines', 'appointment_id', string='appointment lines')
    product_id=fields.Many2one('product.template',string='product template')
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="sale order")
    total_amount=fields.Float(string='Total Amount')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            lines=[(5,0,0)]
            for line in self.product_id.product_variant_ids:
                vals={
                    'product_id': line.id,
                    'product_quantity':5
                }
                lines.append((0,0,vals))
            rec.appointment_lines=lines

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'
    product_id=fields.Many2one('product.product', string='Medicine')
    appointment_id=fields.Many2one('hospital.appointment', string='Appointment id')
    product_quantity=fields.Integer(string='quantity')
    sequence = fields.Integer(string='Sequence')