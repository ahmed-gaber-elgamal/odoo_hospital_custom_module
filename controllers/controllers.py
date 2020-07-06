from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res=super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        print('inherited============================>>>>>>>>', res)
        return res



class Hospital(http.Controller):
    @http.route('/hospital/patient/',website=True, auth='user')
    def hospital_patient(self, **kw):
        patients=request.env['hospital.patient'].sudo().search([])
        return request.render('hospital.patient_page', {
            'patients':patients
        })

    @http.route('/update_patient', type='json', auth="user")
    def update_patient(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                patient=request.env['hospital.patient'].search([("id", "=", rec['id'])])
                if patient:
                    patient.sudo().write(rec)

                args={'success':True, 'message':'success'}
        return args

    @http.route('/create_patient', type='json', auth="user")
    def create_patient(self, **rec):
        if request.jsonrequest:
            print('rec',rec)
            if rec['name']:
                vals={
                    'name' :rec['name']
                }
                new_patient= request.env['hospital.patient'].sudo().create(vals)
                args={'success':True, 'message':'success', 'id':new_patient.id}
        return args

    @http.route('/get_patients', type='json', auth="user")
    def get_patients(self):
        patients_rec=request.env['hospital.patient'].search([])
        patients=[]
        for rec in patients_rec:
            vals={
                'id':rec.id,
                'name':rec.name
            }
            patients.append(vals)
        data = {'status': 200, 'response': patients, 'message': 'success'}
        return data
    @http.route('/hospital/hospital/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('hospital.listing', {
            'root': '/hospital/hospital',
            'objects': http.request.env['hospital.hospital'].search([]),
        })

    @http.route('/hospital/hospital/objects/<model("hospital.hospital"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('hospital.object', {
            'object': obj
        })

    @http.route('/hospital/doctor/', website=True, auth='public')
    def hospital_doctor(self, **kw):
        return 'hello world'
