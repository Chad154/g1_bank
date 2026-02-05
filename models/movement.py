# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Movement(models.Model):
    _name = 'g1.movement'
    _description = 'Movement'

    name = fields.Char()
    
    timestamp = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        readonly=True
    )
    
    amount = fields.Float()
    balance = fields.Float()
    
    description = fields.Selection(
        selection=[
            ('deposit', 'Deposit'),
            ('payment', 'Payment')
        ],
        required=True 
    )
    

    @api.constrains('amount')
    def _check_amount(self):
        for movement in self:
            if movement.amount < 0:
                raise ValidationError("The amount must be greater than zero")
    

    def write(self, vals):
        if 'name' in vals:
            raise ValidationError("You cannot change the name.")

        if 'amount' in vals:
            raise ValidationError("You cannot change the amount.")

        if 'description' in vals:
            raise ValidationError("You cannot change the description.")

        if 'balance' in vals:
            raise ValidationError("You cannot change the balance.")

        return super(Movement, self).write(vals)
    
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
