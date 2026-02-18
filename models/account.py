# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class g1_Account(models.Model):
    _name = 'g1.account'
    _description = 'Bank Account'
    _rec_name = 'id'
	#FIXME Este campo pasa a tener como etiqueta "Descripción"
	#FIXME Su propósito no será almacenar el ID porque ya existe el campo id heredado de models.Model
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
    customer_id = fields.Many2one('res.users', string="Cliente", default=lambda self: self.env.user)
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
    
    #El fixme de credit line negativo esta resuelto aqui
    @api.constrains('account_type', 'credit_line')
    def _check_credit_line(self):
        for account in self:
            if account.account_type == 'standard' and account.credit_line > 0:
                raise ValidationError("Standard accounts cannot have a credit line")
            if account.account_type == 'credit' and account.credit_line <= 0:
                raise ValidationError("Credit accounts must have a credit line greater than 0.")

    #FIXME Verifica que se ejecutan los controles que tienes 
	#en este método cuando se intenta modificar una cuenta
        #METODO modificado, ahora solo verifica los campos necesarios, el de credit line en standard account ya lo hace la vista automaticamente
    def write(self, vals):
        if 'begin_balance' in vals:
            raise ValidationError("You cannot change the initial balance.")
        if 'account_type' in vals:
            raise ValidationError("You cannot change the account type.")

        return super(g1_Account, self).write(vals)
