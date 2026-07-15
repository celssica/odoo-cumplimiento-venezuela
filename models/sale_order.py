from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    l10n_ve_exchange_rate = fields.Float(
        string='Tasa del Día (Bs/USD)',
        digits=(12, 2),
        help='Tasa de cambio USD a Bs para esta cotización',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    )
    l10n_ve_exchange_rate_date = fields.Date(
        string='Fecha de la Tasa',
        readonly=True,
    )
    l10n_ve_amount_total_bs = fields.Monetary(
        string='Total en Bs',
        currency_field='l10n_ve_currency_id',
        compute='_compute_amounts_bs',
        store=True,
    )
    l10n_ve_currency_id = fields.Many2one(
        'res.currency',
        string='Moneda Bs',
        default=lambda self: self.env.ref('base.VES', raise_if_not_found=False),
        readonly=True,
    )

    @api.onchange('date_order')
    def _onchange_date_order(self):
        """Actualizar tasa cuando cambia la fecha"""
        if self.date_order:
            rate = self.env['res.currency'].l10n_ve_get_current_rate()
            if rate:
                self.l10n_ve_exchange_rate = rate
                self.l10n_ve_exchange_rate_date = fields.Date.today()

    @api.depends('amount_total', 'l10n_ve_exchange_rate')
    def _compute_amounts_bs(self):
        for order in self:
            if order.l10n_ve_exchange_rate:
                order.l10n_ve_amount_total_bs = order.amount_total * order.l10n_ve_exchange_rate
            else:
                order.l10n_ve_amount_total_bs = 0.0

    def action_update_exchange_rate(self):
        """Botón para actualizar tasa manualmente"""
        self.ensure_one()
        # Llamar al método en el modelo res.currency con sudo para evitar permisos
        rate = self.env['res.currency'].sudo().l10n_ve_update_rate_yadio()
        if rate:
            self.write({
                'l10n_ve_exchange_rate': rate,
                'l10n_ve_exchange_rate_date': fields.Date.today(),
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Tasa Actualizada',
                    'message': f'Tasa del día: {rate:,.2f} Bs/USD',
                    'type': 'success',
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'No se pudo obtener la tasa del día',
                    'type': 'danger',
                }
            }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    l10n_ve_price_unit_bs = fields.Float(
        string='Precio Unit. Bs',
        digits=(12, 2),
        compute='_compute_price_bs',
        store=True,
    )
    l10n_ve_price_subtotal_bs = fields.Float(
        string='Subtotal Bs',
        digits=(12, 2),
        compute='_compute_price_bs',
        store=True,
    )

    @api.depends('price_unit', 'product_uom_qty', 'order_id.l10n_ve_exchange_rate')
    def _compute_price_bs(self):
        for line in self:
            rate = line.order_id.l10n_ve_exchange_rate
            if rate:
                line.l10n_ve_price_unit_bs = line.price_unit * rate
                line.l10n_ve_price_subtotal_bs = line.price_subtotal * rate
            else:
                line.l10n_ve_price_unit_bs = 0.0
                line.l10n_ve_price_subtotal_bs = 0.0
