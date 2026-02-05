from odoo import api
from odoo import fields
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    middle_initial = fields.Char(string="Middle Initial")
    bank_password = fields.Char(string="Password")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("first_name"):
                vals["name"] = vals["first_name"]
        return super().create(vals_list)

    def write(self, vals):
        if "first_name" in vals:
            vals["name"] = vals.get("first_name") or ""
        return super().write(vals)
