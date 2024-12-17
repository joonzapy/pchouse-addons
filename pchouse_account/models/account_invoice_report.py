from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    total_cost = fields.Float(string="Costo Total")
    price_with_tax = fields.Float(string="Precio con IVA")

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += ", line.total_cost, line.price_with_tax"
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += ", line.total_cost, line.price_with_tax"
        return group_by_str
