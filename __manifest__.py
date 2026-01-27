# -*- coding: utf-8 -*-
{
    'name': "My Bank",

    'summary': """
        Bank application""",

    'description': """
        The application allows a customer to manage their accounts and perform different types of transactions. 
        In addition, there is an admin user who has more rights than a regular user, 
        giving them a higher level of control within the system. 😃️
    """,

    'author': "Conectica",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/g1_bank.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
