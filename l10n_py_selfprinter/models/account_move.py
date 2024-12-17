from odoo import api, fields, models
from datetime import datetime


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_date_time = fields.Datetime(string="Fecha y Hora de Emisión")
    invoice_date_time_str = fields.Char(compute='_compute_inv_dt_str')
    amount_base_iva_10 = fields.Monetary(string="Gravadas 10%", compute="_compute_py_fields")
    amount_base_iva_10_currency = fields.Monetary(
        string="Gravadas 10%",
        help="Gravadas 10% en la moneda de la factura",
        compute="_compute_py_fields")
    amount_iva_10 = fields.Monetary(string="IVA 10%", compute="_compute_py_fields")
    amount_iva_10_currency = fields.Monetary(
        string="IVA 10%",
        help="IVA 10% en la moneda de la factura",
        compute="_compute_py_fields")
    amount_base_iva_5 = fields.Monetary(string="Gravadas 5%", compute="_compute_py_fields")
    amount_base_iva_5_currency = fields.Monetary(
        string="Gravadas 5% Moneda Fact.",
        help="Gravadas 5% en la moneda de la factura",
        compute="_compute_py_fields")
    amount_iva_5 = fields.Monetary(string="IVA 5%", compute="_compute_py_fields")
    amount_iva_5_currency = fields.Monetary(
        string="IVA 5%",
        help="IVA 5% en la moneda de la factura",
        compute="_compute_py_fields")
    amount_exempt = fields.Monetary(string="Exentas", compute="_compute_py_fields")
    amount_exempt_currency = fields.Monetary(
        string="Exentas Moneda Fac.",
        help="Monto de Exentas en la moneda de la factura",
        compute="_compute_py_fields")
    amount_subtotal_5 = fields.Float(string="Subtotal 5", required=False, compute="_compute_py_fields")
    amount_subtotal_10 = fields.Float(string="Subtotal 10", required=False, compute="_compute_py_fields")
    amount_total_pyg = fields.Monetary(string="Total en Gs.", compute="_compute_py_fields")
    
    

    def _compute_inv_dt_str(self):
        for rec in self:
            rec.invoice_date_time_str = ''
            if rec.invoice_date_time:
                rec.invoice_date_time_str = rec.invoice_date_time.strftime('%d/%m/%Y %H:%M')

    def _post(self, soft=True):
        posted = super(AccountMove, self)._post(soft)
        for rec in self:
            now = datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S")
            dt = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
            rec.invoice_date_time = dt
        return posted

    @api.depends('invoice_line_ids', 'amount_total')
    def _compute_py_fields(self):
        for rec in self:
            rec.amount_base_iva_10 = rec.amount_iva_10 = rec.amount_base_iva_5 = rec.amount_iva_5 = \
                rec.amount_exempt = rec.amount_subtotal_5 = rec.amount_subtotal_10 = rec.amount_total_pyg = 0.0

            # IVA 10
            lines = rec.invoice_line_ids.filtered(lambda l: l.tax_ids and l.tax_ids[0].amount == 10)
            rec.amount_base_iva_10 = sum(abs(line.balance) for line in lines)
            rec.amount_base_iva_10_currency = sum(line.amount_currency for line in lines)
            rec.amount_iva_10 = sum((line.price_total - line.price_subtotal) for line in lines)
            rec.amount_iva_10_currency = sum((line.price_total - line.price_subtotal) for line in lines)
                

            # IVA 5
            lines = rec.invoice_line_ids.filtered(lambda l: l.tax_ids and l.tax_ids[0].amount == 5)
            rec.amount_base_iva_5 = sum(abs(line.balance) for line in lines)
            rec.amount_base_iva_5_currency = sum(line.amount_currency for line in lines)  # Para el total en moneda
            rec.amount_iva_5 = sum((line.price_total - line.price_subtotal) for line in lines)
            rec.amount_iva_5_currency = sum((line.price_total - line.price_subtotal) for line in lines)

            # EXENTAS
            amount_exempt = 0.0
            amount_exempt_currency = 0.0
            for line in rec.invoice_line_ids:
                if (line.tax_ids and 'exent' in line.tax_ids[0].name.lower()) or not line.tax_ids:
                    amount_exempt += abs(line.balance)
                    amount_exempt_currency += line.price_total
            rec.amount_exempt = amount_exempt
            rec.amount_exempt_currency = amount_exempt_currency

            # SUBTOTAL
            rec.amount_subtotal_5 = rec.amount_base_iva_5 + rec.amount_iva_5
            rec.amount_subtotal_10 = rec.amount_base_iva_10 + rec.amount_iva_10

            # TOTAL
            rec.amount_total_pyg = rec.currency_id._convert(rec.amount_total, rec.company_currency_id, rec.company_id, rec.invoice_date or rec.date or datetime.today().date())



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    dTasaIVA = fields.Integer(string="Tasa del IVA", compute='_compute_iva_fields')

    def _compute_iva_fields(self):
        for l in self:
            l.dTasaIVA = 0
            if l.tax_ids:
                if '10' in l.tax_ids[0].name:
                    l.dTasaIVA = 10
                elif '5' in l.tax_ids[0].name:
                    l.dTasaIVA = 5
