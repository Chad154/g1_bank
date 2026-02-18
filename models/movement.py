# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
#FIXME redefine el método unlink para permitir borrar solo el último registro de Movement (Metodo creado sobre la clase account)
class Movement(models.Model):
    _name = 'g1.movement'
    _description = 'Movement'

    name = fields.Char(string='Description', required=True)
    timestamp = fields.Date(string='Date', default=fields.Date.context_today, readonly=True)
    amount = fields.Float(required=True)
    balance = fields.Float(string="Balance after movement", readonly=True)
    description = fields.Selection( string='Type of Movement',
        selection=[('deposit', 'Deposit'), ('payment', 'Payment')],
        required=True 
    )
    account_id = fields.Many2one('g1.account', string="Cuenta", required=True)

    @api.constrains('amount')
    def _check_amount(self):
        for movement in self:
            if movement.amount <= 0:
                raise ValidationError("The amount must be greater than zero")
            
    #FIXME: Verifica que se actualiza el saldo de la cuenta al guardar el movimiento.
    @api.model
    def create(self, vals):
        account = self.env['g1.account'].browse(vals.get('account_id'))
        amount = vals.get('amount')
        m_type = vals.get('description')
        
        current_balance = account.balance
        if m_type == 'deposit':
            new_balance = current_balance + amount
        else:
            limit = account.credit_line if account.account_type == 'credit' else 0.0
            if (current_balance + limit) < amount:
                raise ValidationError("Insufficient balance.")
            new_balance = current_balance - amount

        vals['balance'] = new_balance
        
        # Actualizamos el balance y activamos el boton deshacer
        account.sudo().write({
            'balance': new_balance,
            'can_undo_movement': True #  Se activa la posibilidad de deshacer
        })
        return super(Movement, self).create(vals)
        #FIXME: Verifica que no permite hacer UPDATE de estos campos que controlas. (Editados los permisos del csv para q movement no pueda hacer update)
    def write(self, vals):
        if any(f in vals for f in ['name', 'amount', 'description', 'balance', 'account_id']):
            raise ValidationError("Movements cannot be modified once created.")
        return super(Movement, self).write(vals)
