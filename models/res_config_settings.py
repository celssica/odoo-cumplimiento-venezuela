from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_ve_ut_amount = fields.Monetary(
        string='Unidad Tributaria (UT)',
        related='company_id.l10n_ve_ut_amount',
        readonly=False,
        currency_field='currency_id',
        help='Valor de la Unidad Tributaria en VES'
    )
