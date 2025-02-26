{
    'name': 'Clientes',
    'version': '1.0',
    'summary': 'Gestión de clientes',
    'description': 'Módulo para gestionar clientes',
    'category': 'Sales',
    'author': 'Tu Nombre',
    'website': 'https://www.tuwebsite.com',
    'depends': ['base', 'account'],  # Dependemos de 'account' para acceder a la misma funcionalidad de clientes
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
}