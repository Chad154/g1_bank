# -*- coding: utf-8 -*-

from odoo import models, fields
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
    
    def write(self, vals):
        if 'name' in vals:
            raise ValidationError("No puedes editar el Nombre.")

        if 'amount' in vals:
            raise ValidationError("No puedes editar el Monto.")

        if 'description' in vals:
            raise ValidationError("No puedes editar la Descripción.")

        if 'balance' in vals:
            raise ValidationError("No puedes editar el Balance.")

        # Si no se tocó ninguno de los anteriores, guardamos normalmente
        return super(Movement, self).write(vals)
        
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
