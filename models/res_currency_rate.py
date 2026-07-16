import requests
import logging
from datetime import datetime
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    l10n_ve_source = fields.Selection([
        ('manual', 'Manual'),
        ('yadio', 'Yadio.io'),
        ('bcv', 'BCV'),
    ], string='Fuente', default='manual')


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def l10n_ve_update_rate_yadio(self):
        """Actualizar tasa USD/VES usando Yadio.io API"""
        _logger.info("Iniciando actualización de tasa Yadio...")
        try:
            response = requests.get(
                'https://api.yadio.io/rate/USD/VES',
                timeout=10
            )
            _logger.info(f"Respuesta Yadio status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            _logger.info(f"Datos Yadio: {data}")
            
            if data.get('rate'):
                rate = 1.0 / data['rate']  # Invertir porque Odoo guarda rate = 1/tasa
                _logger.info(f"Rate calculado: {rate}")
                
                # Buscar o crear registro de tasa para hoy
                currency_usd = self.env.ref('base.USD')
                currency_ves = self.env.ref('base.VES', raise_if_not_found=False)
                
                if not currency_ves:
                    _logger.error("No se encontró la moneda VES")
                    return False
                
                today = fields.Date.today()
                _logger.info(f"Buscando tasa para fecha: {today}, moneda: {currency_ves.id}")
                
                # Buscar si ya existe tasa para hoy
                existing_rate = self.env['res.currency.rate'].search([
                    ('currency_id', '=', currency_ves.id),
                    ('name', '=', today),
                    ('company_id', '=', self.env.company.id),
                ], limit=1)
                
                if existing_rate:
                    _logger.info(f"Actualizando tasa existente: {existing_rate.id}")
                    existing_rate.write({
                        'rate': rate,
                        'l10n_ve_source': 'yadio',
                    })
                else:
                    _logger.info("Creando nueva tasa")
                    self.env['res.currency.rate'].create({
                        'currency_id': currency_ves.id,
                        'name': today,
                        'rate': rate,
                        'l10n_ve_source': 'yadio',
                        'company_id': self.env.company.id,
                    })
                
                _logger.info(f"Tasa VES actualizada: {data['rate']} Bs/USD")
                return data['rate']
            else:
                _logger.error(f"No se encontró 'rate' en respuesta: {data}")
                return False
            
        except Exception as e:
            _logger.error(f"Error actualizando tasa Yadio: {str(e)}", exc_info=True)
            return False

    def l10n_ve_get_current_rate(self):
        """Obtener tasa actual del VES (Bs/USD).

        Busca la tasa más reciente disponible (fecha <= hoy) y, si no existe
        ninguna, intenta obtenerla en vivo desde Yadio (bootstrap único).
        """
        currency_ves = self.env.ref('base.VES', raise_if_not_found=False)
        if not currency_ves:
            return 0.0

        today = fields.Date.today()
        rate = self.env['res.currency.rate'].search([
            ('currency_id', '=', currency_ves.id),
            ('name', '<=', today),
            ('company_id', 'in', [self.env.company.id, False]),
        ], order='name desc', limit=1)

        if rate and rate.rate:
            return 1.0 / rate.rate  # Devolver tasa directa (Bs/USD)

        # No hay tasa almacenada: intentar obtenerla en vivo
        live = self.l10n_ve_update_rate_yadio()
        return live or 0.0
