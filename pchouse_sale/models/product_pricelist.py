from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    user_groups = fields.Many2many(
        'res.groups',
        string='Grupos de Usuarios',
        help='Especifica los grupos de usuarios que pueden utilizar esta tarifa.'
    )
