from odoo import api, models, fields


class Stamping(models.Model):
    _inherit = 'talonario_py.timbrado'

    autoprint_auth = fields.Char(string="Aut. Autoimpresor", help="Autorización de autoimpresor")
    stamping_type = fields.Selection(selection=[
        ('1', 'PREIMPRESO'),
        ('2', 'VIRTUAL'),
        ('3', 'ELECTRONICO'),
        ('4', 'AUTOIMPRESOR'),
    ], string='Tipo de Timbrado', default='1')