# -*- coding: utf-8 -*-
{
    "name": "My Bank (Customers WP3)",
    "summary": "Customers CRUD (WP3) using res.partner extension",
    "description": """
Customer CRUD for the bank project (WP3).
- Customer is implemented by extending res.partner (Odoo 16).
- Data validations included (email, zip, phone, password, middle initial).
- Customer users can only see/edit their own profile (record rule).
""",
    "author": "Conectica",
    "website": "https://www.yourcompany.com",
    "category": "Finance",
    "version": "16.0.1.0.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/views.xml",
        "views/g1_bank.xml",
        "views/g1_bank_customer.xml",
        "views/templates.xml",
    ],
    "application": True,
    "installable": True,
}
