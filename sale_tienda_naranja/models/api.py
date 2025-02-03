from odoo import models, fields, api
import requests, json
import logging
from requests.exceptions import RequestException
from odoo.exceptions import ValidationError
from requests_oauthlib import OAuth1


_logger = logging.getLogger(__name__)




class TiendaNaranjaApi(models.Model):
    _name = 'tienda.naranja.api'

    name = fields.Char(string="Nombre")
    consumer_key = fields.Char(string="Consumer Key", required=True)
    consumer_secret = fields.Char(string="Consumer Secret", required=True)
    access_token = fields.Char(string="Access Token", required=True)
    access_token_secret = fields.Char(string="Access Token Secret", required=True)
    token_key = fields.Char(string="Token Key", readonly=True)
    username = fields.Char(string="Usuario", required=True)
    password = fields.Char(string="Contraseña", required=True)
    base_url = fields.Char(string="Base URL")

    def request_token(self):
        url = f"{self.base_url}/rest/V1/integration/customer/token"
        try:

            auth = OAuth1(
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
                signature_method='HMAC-SHA256',
                signature_type='auth_header'
            )

            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'username': self.username,
                'password': self.password
            }
            _logger.info(f"URL: {url}")
            _logger.info(f"Headers: {headers}")
            _logger.info(f"Payload: {payload}")

            # Realizar la solicitud POST
            response = requests.post(url, headers=headers, json=payload, auth=auth)
            response.raise_for_status()

            token = response.json()
            self.token_key = token
            return token

        except RequestException as e:
            _logger.error(f"Error al conectar con la API de Tienda Naranja: {e}")
            _logger.error(f"Respuesta del servidor: {e.response.text if e.response else 'No hay respuesta'}")
            raise ValidationError(f"Error al conectar con la API de Tienda Naranja: {e}")
        except json.JSONDecodeError as e:
            _logger.error(f"Error al decodificar la respuesta JSON: {e}")
            raise ValidationError("La respuesta de la API no es un JSON válido.")
        except Exception as e:
            _logger.error(f"Error inesperado: {e}")
            raise ValidationError(f"Error inesperado: {e}")