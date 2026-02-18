# -*- coding: utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import ValidationError
import re


class Customer(models.Model):
    _inherit = "res.users"
    _description = "Customer G1 Bank"

    _EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    _CITY_RE = re.compile(r"^[A-Za-z]+$")

    def _warn(self, title, message):
        return {"warning": {"title": title, "message": message}}

    def _ensure(self, condition, msg):
        if not condition:
            raise ValidationError(msg)


    account_ids = fields.Many2many(
                                   comodel_name="g1.account",
                                   relation="g1_user_account_rel",
                                   column1="user_id",
                                   column2="account_id",
                                   string="Cuentas"
                                   )

    @api.constrains("login")
    def _check_login_is_email(self):
        for user in self:
            if user.login:
                self._ensure(
                             bool(self._EMAIL_RE.fullmatch(user.login)),
                             "El email debe tener el siguiente formato ejemplo@ejemplo.ejemplo",
                             )

    @api.onchange("login")
    def _onchange_login(self):
        if self.login and not self._EMAIL_RE.fullmatch(self.login):
            return self._warn(
                              "Email inválido",
                              "El email debe tener el siguiente formato ejemplo@ejemplo.ejemplo",
                              )

    @api.constrains("city")
    def _check_city_only_letters(self):
        for user in self:
            if user.city:
                self._ensure(
                             bool(self._CITY_RE.fullmatch(user.city)),
                             "La ciudad solo puede contener letras.",
                             )

    @api.onchange("city")
    def _onchange_city(self):
        if self.city and not self._CITY_RE.fullmatch(self.city):
            return self._warn(
                              "Ciudad inválida",
                              "La ciudad solo puede contener letras.",
                              )

    
    @api.constrains("zip")
    def _check_zip_5_digits(self):
        for user in self:
            if user.zip:
                self._ensure(user.zip.isdigit(), "El ZIP solo puede contener números.")

    @api.onchange("zip")
    def _onchange_zip(self):
        if self.zip and (not self.zip.isdigit()):
            return self._warn(
                              "Código postal no válido"
                              )


    @api.constrains("phone")
    def _check_phone_digits(self):
        for user in self:
            if user.phone:
                self._ensure(user.phone.isdigit(), "El teléfono solo debe contener numeros.")

    @api.onchange("phone")
    def _onchange_phone(self):
        if self.phone and not self.phone.isdigit():
            return self._warn(
                              "Teléfono no válido",
                              "Introduce solo numeros",
                              )
