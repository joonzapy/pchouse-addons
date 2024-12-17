from odoo import api, models, fields

class Talonario(models.Model):
    _inherit = "talonario_py.talonario"

    selfprinter_header = fields.Html(string="Datos Autoimpresor")