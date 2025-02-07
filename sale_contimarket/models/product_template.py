from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def prepare_product_data(self):
        """
        Prepara los datos de los productos en el formato requerido por la API.
        :return: Lista de diccionarios con la estructura de productos.
        """
        products = []
        for product in self.product_ids:
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

        
    def action_import_to_contimarket(self):
        """
        Importa los productos seleccionados a ContiMarket.
        """
        # Obtener la configuración de la API
        api_config = self.env['contimarket.api'].search([], limit=1)
        if not api_config:
            raise models.ValidationError("No se encontró la configuración de la API de ContiMarket.")

        # Preparar los datos de los productos
        products = self.prepare_product_data()

        # Llamar al método de importación
        try:
            response = api_config.import_products(products)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Importación exitosa',
                    'message': f"Productos importados correctamente: {response}",
                    'sticky': False,
                }
            }
        except models.ValidationError as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error en la importación',
                    'message': str(e),
                    'sticky': True,
                }
            }