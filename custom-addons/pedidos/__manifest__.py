{
    'name': 'Pedidos',
    'version': '1.0',
    'summary': 'Módulo para gestionar pedidos basados en presupuestos',
    'description': """
        Este módulo permite crear y gestionar pedidos relacionados con presupuestos.
    """,
    'category': 'Sales',
    'author': 'Tu Nombre',
    'depends': ['base', 'mail', 'presupuestos', 'productos', 'account'],  
    'data': [
        'security/ir.model.access.csv',
        'views/pedido_views.xml',
        'data/ir_sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}