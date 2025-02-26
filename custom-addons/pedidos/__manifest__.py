{
    'name': 'Pedidos',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Gestión exclusiva de Pedidos',
    'description': """
        Este módulo crea una nueva aplicación para gestionar exclusivamente pedidos.
        Extiende las órdenes de venta añadiendo un campo para clasificarlas como Pedido.
    """,
    'author': 'Tu Nombre',
    'depends': ['sale_management'],
    'data': [
        'security/pedidos_security.xml',
        'security/ir.model.access.csv',
        'views/pedidos_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}