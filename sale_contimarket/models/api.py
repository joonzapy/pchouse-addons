import base64
import requests
from odoo import models, fields, api


class ContiMarketAPI(models.Model):
    _name = 'contimarket.api'
    _description = 'ContiMarket API'

    url = fields.Char(string='URL', required=True)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)

    def _get_auth_header(self):
        """Genera la cabecera de autenticación Basic."""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return {'Authorization': f'Basic {encoded_credentials}'}

    def make_request(self, endpoint, method='GET', data=None):
        """Realiza una solicitud HTTP a la API de ContiMarket."""
        url = f"{self.api_url}/{endpoint}"
        headers = self._get_auth_header()

        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
            return response.json()  # Retorna la respuesta en formato JSON
        except requests.exceptions.HTTPError as http_err:
            raise models.ValidationError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise models.ValidationError(f"An error occurred: {err}")