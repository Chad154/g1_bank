# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
    _name = 'g1.customer'
    _description = 'Customer'

    name = fields.Char(string="Name")
    last_name = fields.Char(string="Last Name")
    middle_initial = fields.Char(string="Middle Initial")
    street = fields.Char(string="Street")
    state = fields.Char(string="State")
    zip = fields.Integer(string="ZIP")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    password = fields.Char(string="Password")
     
     
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
