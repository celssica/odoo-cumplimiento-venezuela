from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_ve_ut_amount = fields.Monetary(
        string='Unidad Tributaria (UT)',
        currency_field='currency_id',
        help='Valor de la Unidad Tributaria en VES',
        default=0.0
    )
