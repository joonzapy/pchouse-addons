from odoo import models, fields, api
from odoo.exceptions import ValidationError



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                tarifa_base_price = self._get_pricelist_base_price(line.product_id)
                
                if line.price_unit and line.price_unit < tarifa_base_price:
                    raise ValidationError(
                        f"El precio ingresado no puede ser menor que el precio base."
                    )

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        for line in self:
            if not self.env.user.has_group('sales_team.group_sale_manager'):
                if line.product_id:
                    tarifa_base_price = self._get_pricelist_base_price(line.product_id)
                    
                    if line.price_unit < tarifa_base_price:
                        raise ValidationError(
                            f"El precio ingresado no puede ser menor que el precio base."
                        )

    def _get_pricelist_base_price(self, product):
        user_groups = self.env.user.groups_id

        pricelist = self.env['product.pricelist'].search([
            ('user_groups', 'in', user_groups.ids)
        ], limit=1)
        
        if not pricelist:
            raise ValidationError("No se encontró una tarifa base asociada a los grupos del usuario actual.")

        price_base = pricelist.get_product_price(product, 1.0, self.order_id.partner_id)
        
        return price_base
