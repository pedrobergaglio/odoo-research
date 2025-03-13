{
    'name': 'Custom Clients',
    'version': '1.0',
    'summary': 'Custom Client Management Application',
    'description': 'A custom application to manage clients with categories and related orders/services.',
    'category': 'Sales',
    'depends': ['base', 'pedidos', 'servicio_tecnico'],  
    'data': [
        'security/ir.model.access.csv',
        'views/custom_client_views.xml',
    ],
    'installable': True,
    'application': True,
}