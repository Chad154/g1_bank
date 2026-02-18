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
    
    # Campo para controlar el deshacer
    can_undo_movement = fields.Boolean(string="Puede deshacer", default=False)
    
    movement_ids = fields.One2many('g1.movement', 'account_id', string="Movimientos")

    @api.model
    def create(self, vals):
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

    def action_unlink_last_movement(self):
        for account in self:
            # Si el boton esta apagado, no deja borrar
            if not account.can_undo_movement:
                raise ValidationError("You can only undo the last movement")

            last_move = self.env['g1.movement'].search([
                ('account_id', '=', account.id)
            ], order='id desc', limit=1)

            if not last_move:
                account.can_undo_movement = False
                raise ValidationError("There is no movement to undo.")

            # Revertimos el balance
            if last_move.description == 'deposit':
                new_balance = account.balance - last_move.amount
            else:
                new_balance = account.balance + last_move.amount

            # Actualizamos cuenta, apagamos el boton y borramos
            account.sudo().write({
                'balance': new_balance,
                'can_undo_movement': False  # Bloqueamos el siguiente intento
            })
            last_move.unlink()
        return True
