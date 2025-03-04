{
    'name': 'Presupuestos',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Gestión centralizada de Presupuestos',
    'description': """
        Este módulo crea una nueva aplicación para gestionar presupuestos de forma centralizada.
        Permite categorizar los presupuestos como Pedidos o Servicios Técnicos.
    """,
    'author': 'Tu Nombre',
    'depends': ['sale_management', 'pedidos', 'servicio_tecnico'],
    'data': [
        'security/presupuestos_security.xml',
        'security/ir.model.access.csv',
        'views/presupuestos_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}