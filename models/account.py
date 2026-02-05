# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class g1_Account(models.Model):
    _name = 'g1.account'
    _description = 'g1.account'

    name = fields.Char(string="Número de Cuenta")
    description = fields.Text(string="Descripción")
    account_type = fields.Selection(
        selection=[
            ('standard', 'Estándar'),
            ('credit', 'Crédito')
        ],
        string="Tipo de Cuenta",
        required=True,
    )
    balance = fields.Float(string="Balance Actual", default=0.0)
    credit_line = fields.Float(string="Línea de Crédito")
    opening_date = fields.Date(string="Fecha de Apertura", default=fields.Date.context_today, readonly=True)
    begin_balance = fields.Float(string="Balance Inicial")
    
    
    @api.constrains('begin_balance', 'credit_line')
    def _check_positive_amounts(self):
        for account in self:
            if account.begin_balance < 0:
                raise ValidationError("The initial balance must be greater than or equal to zero.")
            if account.credit_line < 0:
                raise ValidationError("The line of credit cannot be negative.")
    
            
    @api.constrains('account_type', 'credit_line')
    def _check_credit_line(self):
        for account in self:
            if account.account_type == 'standard' and account.credit_line > 0:
                raise ValidationError("Standard accounts cannot have a credit line")
                
    @api.model
    def create(self, vals):
        # Si ponen un balance inicial, el balance actual debe arrancar igual
        if 'begin_balance' in vals:
            vals['balance'] = vals['begin_balance']
        return super(g1_Account, self).create(vals)
    
    
    def write(self, vals):
        if 'name' in vals:
            raise ValidationError("You cannot change the name.")

        if 'begin_balance' in vals:
            raise ValidationError("You cannot change the initial balance.")

        if 'balance' in vals:
            raise ValidationError("You cannot change the balance.")
        
        if 'account_type' in vals:
            raise ValidationError("You cannot change the account type.")
        
        if 'credit_line' in vals:
            for record in self:
                if record.account_type == 'standard':
                    raise ValidationError(
                        "You cannot change the credit line in a standard account"
                    )

        return super(g1_Account, self).write(vals)
    

    # Relación N:1 con Customer
    # customer_id = fields.Many2one('g1.customer', string="Cliente")
    
    # Relación 1:N con Movimientos
    # movement_ids = fields.One2many('g1.movement', 'account_id', string="Movimientos")