# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
    opening_date = fields.Date(string="Fecha de Apertura", default=fields.Date.context_today)
    begin_balance = fields.Float(string="Balance Inicial")
    

    # Relación N:1 con Customer
    # customer_id = fields.Many2one('g1.customer', string="Cliente")
    
    # Relación 1:N con Movimientos
    # movement_ids = fields.One2many('g1.movement', 'account_id', string="Movimientos")