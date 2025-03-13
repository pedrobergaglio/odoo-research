{
    'name': 'Productos',
    'version': '1.0',
    'summary': 'Gestión de productos personalizada',
    'description': """
        Aplicación para gestionar productos de forma independiente al módulo stock.
        Incluye gestión de categorías y productos con precios y cantidades.
    """,
    'author': 'Tu Nombre',
    'category': 'Inventory',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/productos_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}