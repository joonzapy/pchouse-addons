# -*- coding: utf-8 -*-
# from odoo import http


# class L10nPySelfprinter(http.Controller):
#     @http.route('/l10n_py_selfprinter/l10n_py_selfprinter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_py_selfprinter/l10n_py_selfprinter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_py_selfprinter.listing', {
#             'root': '/l10n_py_selfprinter/l10n_py_selfprinter',
#             'objects': http.request.env['l10n_py_selfprinter.l10n_py_selfprinter'].search([]),
#         })

#     @http.route('/l10n_py_selfprinter/l10n_py_selfprinter/objects/<model("l10n_py_selfprinter.l10n_py_selfprinter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_py_selfprinter.object', {
#             'object': obj
#         })
