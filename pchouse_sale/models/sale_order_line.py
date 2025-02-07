from odoo import models, fields, api
from odoo.exceptions import ValidationError



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        self._validate_price_unit()
        return res
    
    @api.model
    def create(self, vals):
        record = super(SaleOrderLine, self).create(vals)
        record._validate_price_unit()
        return record
    
    def _validate_price_unit(self):
        for line in self:
            if self.env.user.has_group('pchouse_sale.group_allow_below_base_price'):
            # Si el usuario pertenece al grupo, omitir la validación
                continue
            if line.product_id:
                partner_pricelist = line.order_id.partner_id.property_product_pricelist
                if partner_pricelist and partner_pricelist.id != 28:
                    # Si el cliente tiene una tarifa especial asignada, se usa sin restricciones
                    return
                # Si el cliente no tiene una tarifa especial, aplicar la tarifa por grupo del vendedor
                tarifa_base_price = line._get_pricelist_base_price(line.product_id)
                if line.price_unit < tarifa_base_price:
                    raise ValidationError(
                        f"El precio en la línea para el producto '{line.product_id.name}' "
                        f"({line.price_unit}) no puede ser menor que el precio base ({tarifa_base_price})."
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
