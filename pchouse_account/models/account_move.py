from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    total_cost = fields.Monetary(
        string="Costo Total",
        compute="_compute_total_cost",
        store=True,
        currency_field="currency_id",
        groups="pchouse_account.group_account_admin",
    )

    def action_post(self):
        """al confirmar la factura se actualiza el campo
        historical_cost de las lineas y también el campo total_cost."""
        self._update_historical_cost()
        super(AccountMove, self).action_post()


    @api.depends('invoice_line_ids', 'invoice_line_ids.historical_cost', 'invoice_line_ids.product_id', 'invoice_line_ids.quantity')
    def _compute_total_cost(self):
        for move in self:
            total_cost = 0.0
            for line in move.invoice_line_ids:
                if line.product_id:
                    total_cost += line.line_total_cost
            
            move.total_cost = total_cost


    def _update_historical_cost(self):
        for move in self:
            for line in move.invoice_line_ids:
                if line.product_id:
                    line.historical_cost = line.product_id.standard_price

    @api.model
    def create(self, vals):
        """al crear una factura, se asigna un valor al campo historical_cost
        de las lineas y el campo total_cost se actualiza."""
        move = super(AccountMove, self).create(vals)
        for line in move.invoice_line_ids:
            if line.product_id and not line.historical_cost:
                line.historical_cost = line.product_id.standard_price
        return move

    def write(self, vals):
        """si la factura está en modo borrador y luego se modifica,
        el campo historical_cost de las líneasse actualiza, también el campo total_cost."""
        res = super(AccountMove, self).write(vals)
        
        if self.filtered(lambda move: move.state == 'draft'):
            self._update_historical_cost()
        return res



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    historical_cost = fields.Monetary(
        string="Costo Histórico",
        currency_field="currency_id"
    )
    price_with_tax = fields.Float(string="Precio con IVA", compute="_compute_price_with_tax", store=True)
    line_total_cost = fields.Monetary(
        string="Costo total",
        compute="_compute_line_total_cost",
        store=True,
        currency_field="currency_id"
    )

    @api.depends('historical_cost', 'quantity')
    def _compute_line_total_cost(self):
        for line in self:
            line.line_total_cost = line.historical_cost * line.quantity

    @api.depends('price_subtotal', 'tax_ids')
    def _compute_price_with_tax(self):
        for line in self:
            taxes = line.tax_ids.compute_all(
                line.price_unit,
                line.move_id.currency_id,
                line.quantity,
                product=line.product_id)
            line.price_with_tax = taxes['total_included']