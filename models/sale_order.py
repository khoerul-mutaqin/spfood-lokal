from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"
      
    x_discount = fields.Monetary(string="Discount", store=True, compute='_compute_x_discount')
    x_amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_compute_x_amount_untaxed')
    
    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'payment_term_id')
    def _compute_x_discount(self):
        x_discount = 0
        for order in self:
            discount_line = self.order_line.filtered(lambda x: x.price_subtotal < 0)
            #discount line 
            for line in discount_line:
                x_discount += line.price_subtotal
            order['x_discount'] = x_discount

    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'payment_term_id')
    def _compute_x_amount_untaxed(self):
        x_amount_untaxed = 0
        for order in self:
            untaxed_line = self.order_line.filtered(lambda x: x.price_subtotal > 0)
            #untaxed line 
            for line in untaxed_line:
                x_amount_untaxed += line.price_subtotal
            order['x_amount_untaxed'] = x_amount_untaxed
