from odoo import models, fields, api
import requests, json


class TiendaNaranjaApi(models.Model):
    _name = 'tienda.naranja.api'

    name = fields.Char(string="Nombre")
    token_key = fields.Char(string="Token Key", readonly=True)
    username = fields.Char(string="Usuario", required=True)
    password = fields.Char(string="Contraseña", required=True)
    base_url = fields.Char(string="Base URL")

    def request_token(self):
        """
        Solicita un token de acceso a la API de Tienda Naranja.
        Registra el resultado en los logs.
        :return: Token de acceso.
        """
        try:
            self.ensure_one()
            
            # URL para el endpoint de autenticación
            url = f"{self.base_url}/rest/V1/integration/customer/token"
            
            # Headers y contenido para la solicitud
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            content = {'username': self.username, 'password': self.password}
            
            # Realizar la solicitud POST
            response = requests.post(url, headers=headers, json=content)
            
            # Manejar errores de la respuesta
            if response.status_code != 200:
                raise Exception(f'Status Code: {response.status_code}, Reason: {response.reason}')
            
            # Extraer el token de la respuesta
            data = response.json()
            token = data.get('token')
            if not token:
                raise Exception("No se recibió un token en la respuesta.")
            
            self.write({'token_key': token})
            
            # Registrar en el log
            self.create_log("Se obtuvo un nuevo token y se actualizó token_key", "INFO", 'request_token')
            
            return token
        
        except Exception as error:
            # Manejo de errores
            self.create_log(f"Error al solicitar el token: {error}", "ERROR", 'request_token')
            raise

    def get_products(self, token):
        self.ensure_one()
        url = f"{self.base_url}/rest/V1/products"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            raise ValueError(f"Error al obtener productos: {response.status_code} - {response.text}")