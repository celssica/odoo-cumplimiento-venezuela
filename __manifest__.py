{
    'name': 'Cumplimiento SENIAT Venezuela',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Localización Venezuela para Odoo 17 - Retenciones, ISLR, IVA, Facturación',
    'description': """
        Módulo de localización venezolana para Odoo 17
        ==============================================
        
        Características:
        - Plan de cuentas básico Venezuela
        - Impuestos: IVA 16%, Retenciones IVA 75%/100%
        - ISLR: Conceptos y retenciones
        - Unidad Tributaria (UT) configurable
        - Campos RIF y número de control en facturas
        - Reportes: Libro de compras, Libro de ventas
        
        Desarrollado por CELSSICA
    """,
    'author': 'CELSSICA',
    'website': 'https://celssica.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'sale',
        'l10n_latam_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/account_tax_data.xml',
        'data/res_currency_data.xml',
        'data/ir_cron_data.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
