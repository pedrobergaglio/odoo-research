{
    'name': 'Presupuestos',
    'version': '1.0',
    'summary': 'Gestión de Presupuestos',
    'description': """
        Módulo para gestionar presupuestos que pueden convertirse en pedidos o servicios técnicos.
    """,
    'category': 'Sales',
    'author': 'Tu Empresa',
    'website': 'https://www.tuempresa.com',
    'depends': ['base', 'mail', 'productos', 'account',],
    'data': [
        'security/presupuesto_security.xml',
        'security/ir.model.access.csv',
        'data/presupuesto_sequence.xml',
        'data/presupuesto_data.xml',
        'views/presupuesto_views.xml',
    ],
    'assests': {
        'web.assets_backend': [
            'static/src/js/custom_statusbar.js'
        ],
    },

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}