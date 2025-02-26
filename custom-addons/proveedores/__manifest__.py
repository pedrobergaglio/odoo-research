{
    'name': 'Proveedores',
    'version': '1.0',
    'summary': 'Gestión de proveedores',
    'description': 'Módulo para gestionar proveedores',
    'category': 'Purchase',
    'author': 'Tu Nombre',
    'website': 'https://www.tuwebsite.com',
    'depends': ['base', 'account'],  # Dependemos de 'account' para acceder a la funcionalidad de proveedores
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
}