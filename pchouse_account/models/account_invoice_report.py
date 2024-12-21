from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    currency_id = fields.Many2one('res.currency', string="Moneda", readonly=True)
    line_total_cost = fields.Monetary(string="Costo Total", readonly=True, currency_field='currency_id')
    price_with_tax = fields.Monetary(string="Precio con IVA", readonly=True, currency_field='currency_id')

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += ", line.line_total_cost, line.price_with_tax"
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += ", line.line_total_cost, line.price_with_tax"
        return group_by_str
