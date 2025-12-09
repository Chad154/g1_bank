# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
     _name = 'g1_bank.customer'
     _description = 'Customer'

     name = fields.Char()
     firstName = fields.String
     lastName = fields.String
     middleInitial = fields.Char
     Street = fields.String
     State = fields.String
     zip = fields.Integer
     phone = fields.Integer
     email = fields.String
     password = fields.String
     
     
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
