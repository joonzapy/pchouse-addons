from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    line_total_cost = fields.Char(string="Costo Total")
    price_with_tax = fields.Char(string="Precio con IVA")

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += ", line.line_total_cost, line.price_with_tax"
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += ", line.line_total_cost, line.price_with_tax"
        return group_by_str
