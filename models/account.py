# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class g1_Account(models.Model):
    _name = 'g1.account'
    _description = 'Bank Account'
	#FIXME Este campo pasa a tener como etiqueta "Descripción"
	#FIXME Su propósito no será almacenar el ID porque ya existe el campo id heredado de models.Model
    name = fields.Char(string="Número de Cuenta", required=True)
    #FIXME Eliminar este campo del modelo y de las vistas
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
	#FIXME añade campo relacional con res.users y asocia la cuenta con el usuario que está creando la cuenta cuando
	#esta última se cree
	
	#FIXME añade validación para no admitir credit_line negativo
	
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
	#FIXME Añade la anotación api.model y verifica que se ejecutan los controles que tienes 
	#en este método cuando se intenta modificar una cuenta
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