{
    'name': 'Servicio Tecnico',
    'version': '1.0',
    'summary': 'Módulo para gestionar servicios tecnicos basados en presupuestos',
    'description': """
        Este módulo permite crear y gestionar servicios tecnicos relacionados con presupuestos.
    """,
    'category': 'Sales',
    'author': 'Tu Nombre',
    'depends': ['base', 'mail', 'presupuestos', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/servicio_tecnico_views.xml',
        'data/ir_sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}