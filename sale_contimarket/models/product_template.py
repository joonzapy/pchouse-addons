from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_available = fields.Float(string="Cantidad a mano", compute='_compute_qty_available')

    @api.depends('product_variant_ids.qty_available')
    def _compute_qty_available(self):
        for template in self:
            template.qty_available = sum(template.product_variant_ids.mapped('qty_available'))