# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class g1_Account(models.Model):
    _name = 'g1.account'
    _description = 'Bank Account'

    name = fields.Char(string="Número de Cuenta", required=True)
    description = fields.Text(string="Descripción")
    account_type = fields.Selection(
        selection=[
            ('standard', 'Estándar'),
            ('credit', 'Crédito')
        ],
        string="Tipo de Cuenta",
        required=True,
    )
    balance = fields.Float(string="Balance Actual", default=0.0, readonly=True)
    credit_line = fields.Float(string="Línea de Crédito")
    opening_date = fields.Date(string="Fecha de Apertura", default=fields.Date.context_today, readonly=True)
    begin_balance = fields.Float(string="Balance Inicial")
    
    # Relacion, cuenta tiene muchos movimientos
    movement_ids = fields.One2many('g1.movement', 'account_id', string="Movimientos")

    @api.model
    def create(self, vals):
        # Al crear la cuenta, inicializamos el balance con el begin_balance
        if 'begin_balance' in vals:
            vals['balance'] = vals['begin_balance']
        return super(g1_Account, self).create(vals)

    @api.constrains('begin_balance')
    def _check_amount(self):
        for account in self:
            if account.begin_balance < 0:
                raise ValidationError("The balance must be greater than zero")
                
    @api.constrains('account_type', 'credit_line')
    def _check_credit_line(self):
        for account in self:
            if account.account_type == 'standard' and account.credit_line > 0:
                raise ValidationError("Standard accounts cannot have a credit line")

    def write(self, vals):
        if 'name' in vals:
            raise ValidationError("You cannot change the name.")
        if 'begin_balance' in vals:
            raise ValidationError("You cannot change the initial balance.")
        if 'account_type' in vals:
            raise ValidationError("You cannot change the account type.")
        
        if 'credit_line' in vals:
            for record in self:
                if record.account_type == 'standard':
                    raise ValidationError("You cannot change the credit line in a standard account")

        return super(g1_Account, self).write(vals)