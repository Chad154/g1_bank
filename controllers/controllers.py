# -*- coding: utf-8 -*-
# from odoo import http


# class G1Bank(http.Controller):
#     @http.route('/g1_bank/g1_bank', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/g1_bank/g1_bank/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('g1_bank.listing', {
#             'root': '/g1_bank/g1_bank',
#             'objects': http.request.env['g1_bank.g1_bank'].search([]),
#         })

#     @http.route('/g1_bank/g1_bank/objects/<model("g1_bank.g1_bank"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('g1_bank.object', {
#             'object': obj
#         })
