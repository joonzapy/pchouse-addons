from odoo import models, fields, api
import requests, json


class TiendaNaranjaApi(models.Model):
    _name = 'tienda.naranja.api'

    name = fields.Char(string="Nombre")
    consumer_key = fields.Char(string="Consumer Key", required=True)
    consumer_secret = fields.Char(string="Consumer Secret", required=True)
    token_key = fields.Char(string="Token Key", required=True)
    token_secret = fields.Char(string="Token Secret", required=True)
    username = fields.Char(string="Usuario", required=True)
    password = fields.Char(string="Contraseña", required=True)
    environment = fields.Selection([
        ('staging', 'Staging'),
        ('production', 'Producción')
    ], string="Entorno", required=True, default='staging')
    base_url = fields.Char(string="Base URL", compute="_compute_base_url")

    @api.depends('environment')
    def _compute_base_url(self):
        for record in self:
            record.base_url = 'https://mcstaging.tiendanaranja.com.py' if record.environment == 'staging' else 'https://tiendanaranja.com.py'

    def get_access_token(self):
        self.ensure_one()
        url = f"{self.base_url}/rest/V1/integration/customer/token"
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'username': self.token_key,
            'password': self.token_secret,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error en autenticación: {response.status_code} - {response.text}")

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