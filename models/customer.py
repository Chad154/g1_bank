# -*- coding: utf-8 -*-

from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import ValidationError
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class ResPartnerCustomer(models.Model):
    _inherit = "res.partner"

    # Campos del enunciado “Customer”
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    middle_initial = fields.Char(string="Middle Initial")
    bank_password = fields.Char(string="Password")

    # ------------------------------
    # Name automático (simple)
    # ------------------------------
    @api.onchange("first_name", "last_name")
    def _onchange_build_name(self):
        for rec in self:
            fn = (rec.first_name or "").strip()
            ln = (rec.last_name or "").strip()
            full = (fn + " " + ln).strip()
            if full:
                rec.name = full

    @api.model
    def create(self, vals):
        # si no viene name, lo construimos con first/last
        if not vals.get("name"):
            fn = (vals.get("first_name") or "").strip()
            ln = (vals.get("last_name") or "").strip()
            full = (fn + " " + ln).strip()
            if full:
                vals["name"] = full
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        # si cambian first/last, actualizamos name
        if "first_name" in vals or "last_name" in vals:
            for rec in self:
                fn = (rec.first_name or "").strip()
                ln = (rec.last_name or "").strip()
                full = (fn + " " + ln).strip()
                if full and rec.name != full:
                    super(ResPartnerCustomer, rec).write({"name": full})
        return res

    # ------------------------------
    # Validaciones lógicas (nivel DAM)
    # ------------------------------
    @api.onchange("email")
    def _onchange_email(self):
        for rec in self:
            if rec.email:
                rec.email = rec.email.strip().lower()

    @api.constrains("email")
    def _check_email(self):
        for rec in self:
            e = (rec.email or "").strip()
            if e and not EMAIL_RE.match(e):
                raise ValidationError("Email format is not valid (example: name@mail.com).")

    @api.constrains("middle_initial")
    def _check_middle_initial(self):
        for rec in self:
            mi = (rec.middle_initial or "").strip()
            if mi and (len(mi) != 1 or not mi.isalpha()):
                raise ValidationError("Middle Initial must be exactly 1 letter (A-Z).")

    @api.constrains("zip")
    def _check_zip(self):
        for rec in self:
            z = (rec.zip or "").strip()
            # ZIP España típico: 5 dígitos
            if z and (not z.isdigit() or len(z) != 5):
                raise ValidationError("ZIP must be exactly 5 digits.")

    @api.constrains("phone")
    def _check_phone(self):
        for rec in self:
            p = (rec.phone or "").strip()
            if not p:
                continue
            digits = "".join(ch for ch in p if ch.isdigit())
            if len(digits) < 9 or len(digits) > 15:
                raise ValidationError("Phone must contain between 9 and 15 digits.")

    @api.constrains("bank_password")
    def _check_password(self):
        for rec in self:
            pw = rec.bank_password or ""
            if pw and len(pw) < 8:
                raise ValidationError("Password must have at least 8 characters.")
