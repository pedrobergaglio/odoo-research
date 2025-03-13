{
    'name': 'Custom Proveedores',
    'version': '1.0',
    'summary': 'Gestión de Proveedores Personalizados',
    'description': 'Módulo para gestionar proveedores personalizados.',
    'category': 'Purchases',
    'depends': ['base', 'mail', 'clientes'],  # Dependemos de custom_clientes para la relación
    'data': [
        'security/ir.model.access.csv',
        'views/custom_proveedor_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}