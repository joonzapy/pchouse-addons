from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_free_product = fields.Boolean(string="Libre", help="Permite usar este producto para cotizaciones libres.")
