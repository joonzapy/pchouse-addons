import base64
import requests
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ContiMarketAPI(models.Model):
    _name = 'contimarket.api'
    _description = 'ContiMarket API'

    name = fields.Char(string='Name', required=True)
    url = fields.Char(string='URL', required=True)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)
    product_ids = fields.Many2many('product.template', string="Productos a Importar")

    def _get_auth_header(self):
        """Genera la cabecera de autenticación Basic."""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return {'Authorization': f'Basic {encoded_credentials}'}

    def _prepare_product_data(self):
        """
        Prepara los datos de los productos en el formato requerido por la API.
        :return: Lista de diccionarios con la estructura de productos.
        """
        products = []
        for product in self.product_ids:
            caracteristicas = []
            for attribute_line in product.attribute_line_ids:
                attribute_name = attribute_line.attribute_id.name
                attribute_values = ', '.join(attribute_line.value_ids.mapped('name'))
                caracteristicas.append({
                    'Title': attribute_name,
                    'Value': attribute_values,
                })
            imagenes = []
            if product.image_1920:
                imagen_url = f"/web/image/product.product/{product.id}/image_1920"
                imagenes.append({
                    'url': imagen_url,
                })

            product_data = {
                'CodigoProducto': product.default_code or '',
                'Nombre': product.name,
                'DescripcionBreve': product.description or '',
                'DescripcionCompleta': product.description or '',
                'PrecioCatalogo': product.list_price or 0.0,
                'PrecioContinental': product.list_price or 0.0,
                'Stock': product.qty_available,
                'Peso': 0,
                'Longitud': 0,
                'Anchura': 0,
                'Altura': 0,
                'Caracteristicas': caracteristicas,
                'Imagen': imagenes,
                # Agrega más campos según la documentación de la API
            }
            products.append(product_data)
        return products

    def import_products(self):
        endpoint = 'ImportProduct'
        url = f"{self.url}/{endpoint}"
        headers = self._get_auth_header()
        products = self._prepare_product_data()

        if not products:
            raise models.ValidationError("No hay productos seleccionados para importar.")

        try:
            response = requests.post(url, headers=headers, json=products)
            response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
            result = response.json()

            if not result.get('success', True):
                raise models.ValidationError(f"Error en la importación: {result.get('message', 'Error desconocido')}")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Importación exitosa',
                    'message': f"Productos importados correctamente: {len(products)}",
                    'sticky': False,
                }
            }
        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"HTTP error occurred: {http_err}")
            raise models.ValidationError(f"HTTP error: {http_err}")
        except Exception as err:
            _logger.error(f"An error occurred: {err}")
            raise models.ValidationError(f"Error: {err}")