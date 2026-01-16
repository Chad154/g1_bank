# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
    _name = 'g1.customer'
    _description = 'Customer'

    name = fields.Char(string="Nombre completo")
    first_name = fields.Char(string="Nombre")
    last_name = fields.Char(string="Apellidos")
    middle_initial = fields.Char(string="Inicial")
    street = fields.Char(string="Calle")
    state = fields.Char(string="Estado")
    zip = fields.Integer(string="Código Postal")
    phone = fields.Char(string="Teléfono")
    email = fields.Char(string="Email")
    password = fields.Char(string="Contraseña")
     
     
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
