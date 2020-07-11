# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        educational purpose
    """,

    'author': "Ahmed Gaber",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Educational',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale', 'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_appointment.xml',
        'views/views.xml',
        'views/appointment.xml',
        'data/sequence.xml',
        'data/email_template.xml',
        'views/css_loader.xml',
        'views/settings.xml',
        'views/sale_order.xml',
        'views/templates.xml',
        'reports/report.xml',
        "reports/sale_report_inherit.xml",
        'data/data.xml',
        'data/cron.xml',
        'views/doctor.xml',
        'views/website_form.xml',
        'views/server_action.xml',
        'views/lab.xml',
        'views/dashboard.xml',
        'security/security.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application' : True,

    'css': ['static/src/css/hospital.css'],
}
