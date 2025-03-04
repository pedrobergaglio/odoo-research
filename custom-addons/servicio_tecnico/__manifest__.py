{
    'name': 'Servicio Técnico',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestión exclusiva de Servicios Técnicos',
    'description': """
        Este módulo crea una nueva aplicación para gestionar exclusivamente servicios técnicos.
        Extiende las órdenes de venta añadiendo un campo para clasificarlas como Servicio Técnico.
    """,
    'author': 'Tu Nombre',
    'depends': ['sale_management', 'sale'],
    'data': [
        'security/servicio_tecnico_security.xml',
        'security/ir.model.access.csv',
        'views/servicio_tecnico_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}
