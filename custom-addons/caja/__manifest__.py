{
    'name': 'Caja',
    'version': '1.0',
    'summary': 'Gestión de movimientos de caja',
    'description': 'Módulo para gestionar movimientos de caja con diferentes métodos de pago',
    'author': 'Tu Nombre',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/caja_views.xml',
    ],
    'installable': True,
    'application': True,
}