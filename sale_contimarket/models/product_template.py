from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def prepare_product_data(self):
        """
        Prepara los datos de los productos en el formato requerido por la API.
        :return: Lista de diccionarios con la estructura de productos.
        """
        products = []
        for product in self:
            product_data = {
                'CodigoProducto': product.default_code or '',
                'Nombre': product.name,
                'DescripcionBreve': product.description_sale or '',
                'PrecioCatalogo': product.list_price or '',
                'Stock': product.qty_available,
                # Agrega más campos según la documentación de la API
            }
            products.append(product_data)
        return products