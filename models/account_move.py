from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_ve_control_number = fields.Char(
        string='Número de Control',
        help='Número de control para facturación fiscal en Venezuela'
    )
    l10n_ve_z_report = fields.Char(
        string='Reporte Z',
        help='Número de reporte Z (para punto de venta)'
    )
