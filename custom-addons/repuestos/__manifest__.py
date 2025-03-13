{
    'name': 'Repuestos',
    'version': '1.0',
    'depends': ['base', 'productos'],
    'data': [
        'security/ir.model.access.csv',
        'views/repuestos_views.xml',
        'data/repuestos_data.xml',
    ],
    'installable': True,
    'application': True,
}