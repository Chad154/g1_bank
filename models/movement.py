# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Movement(models.Model):
    _name = 'g1.movement'
    _description = 'Movement'

    name = fields.Char(required=True)
    timestamp = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        readonly=True
    )
    
    amount = fields.Float(required=True)
    balance = fields.Float(string="Balance after movement", readonly=True)
    
    description = fields.Selection(
        selection=[
            ('deposit', 'Deposit'),
            ('payment', 'Payment')
        ],
        required=True 
    )

    # Relacion de movimiento a una cuenta especifica
    account_id = fields.Many2one('g1.account', string="Cuenta", required=True)

    @api.constrains('amount')
    def _check_amount(self):
        for movement in self:
            if movement.amount <= 0:
                raise ValidationError("The amount must be greater than zero")

    @api.model
    def create(self, vals):
        # Usar la cuenta relacionada
        account = self.env['g1.account'].browse(vals.get('account_id'))
        amount = vals.get('amount')
        m_type = vals.get('description')
        
        # Calculo
        current_balance = account.balance
        if m_type == 'deposit':
            new_balance = current_balance + amount
        else: # Si no es deposit es payment
            # Validar si tiene saldo + línea de crédito suficiente
            limit = account.credit_line if account.account_type == 'credit' else 0.0
            if (current_balance + limit) < amount:
                raise ValidationError("Insufficient balance (including line of credit if applicable).")
            new_balance = current_balance - amount

        # Guardamos el balance en movimiento
        vals['balance'] = new_balance
        
        # Actualizamos balance en la cuenta
        # Usamos sudo para asegurar que el sistema puede escribir el balance aunque sea readonly
        account.sudo().write({'balance': new_balance})
        
        return super(Movement, self).create(vals)

    def write(self, vals):
        # Bloqueamos cualquier edición de movimientos ya creados
        if any(f in vals for f in ['name', 'amount', 'description', 'balance', 'account_id']):
            raise ValidationError("Movements cannot be modified once created.")
        return super(Movement, self).write(vals)