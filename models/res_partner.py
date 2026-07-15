from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_ve_rif = fields.Char(
        string='RIF',
        help='Registro de Identificación Fiscal (Venezuela)'
    )
    l10n_ve_responsibility_type = fields.Selection([
        ('ordinary', 'Ordinario'),
        ('special', 'Especial'),
        ('exempt', 'Exento'),
    ], string='Tipo de Responsabilidad')
