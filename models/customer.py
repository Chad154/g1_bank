# -*- coding: utf-8 -*-
from odoo import models

class G1Customer(models.Model):
     _inherit = 'res.users'
     account_ids=fields.Many2many('g3_bank.account',
                                  #Solo muestran las cuentas que tengan saldo inicial y no esten asignadas a un cliente
                                  domain=[('customer_ids', '=', False),('balance','>',0)],
                                  string='Cuentas con Saldo Inicial'
                                  )
