from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    total_cost = fields.Monetary(
        string="Total de Costo",
        compute="_compute_total_cost",
        store=True,
        currency_field="currency_id"
    )

    @api.depends('invoice_line_ids', 'invoice_line_ids.product_id', 'invoice_line_ids.quantity')
    def _compute_total_cost(self):
        for move in self:
            total_cost = 0.0
            for line in move.invoice_line_ids:
                if line.product_id:
                    total_cost += line.historical_cost * line.quantity
            
            move.total_cost = total_cost


    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        for line in move.invoice_line_ids:
            if line.product_id:
                line.historical_cost = line.product_id.standard_price
        return move



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    historical_cost = fields.Monetary(
        string="Costo Histórico",
        currency_field="currency_id"
    )