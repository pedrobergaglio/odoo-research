{
    'name': 'Price Update by Category',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Actualizar precios de productos por categoría',
    'description': """
        Módulo para actualizar precios de productos basado en su categoría y un porcentaje.
    """,
    'depends': ['stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/price_update_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
