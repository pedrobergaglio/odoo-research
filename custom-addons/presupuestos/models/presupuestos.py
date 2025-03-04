from odoo import models, fields, api

class PresupuestoCategory(models.Model):
    _name = 'presupuesto.category'
    _description = 'Categoría de Presupuesto'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)
    description = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)
    
    # Campo para identificar si es un pedido o servicio técnico
    type = fields.Selection([
        ('pedido', 'Pedido'),
        ('servicio', 'Servicio Técnico')
    ], string='Tipo', required=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    presupuesto_category_id = fields.Many2one('presupuesto.category', string='Categoría', 
                                          tracking=True,
                                          help="Categoriza este presupuesto como Pedido o Servicio Técnico")
    is_pedido_presupuesto = fields.Boolean('Es Pedido', compute='_compute_presupuesto_type', store=True)
    is_servicio_presupuesto = fields.Boolean('Es Servicio Técnico', compute='_compute_presupuesto_type', store=True)
    
    @api.depends('presupuesto_category_id', 'presupuesto_category_id.type')
    def _compute_presupuesto_type(self):
        for order in self:
            order.is_pedido_presupuesto = order.presupuesto_category_id.type == 'pedido' if order.presupuesto_category_id else False
            order.is_servicio_presupuesto = order.presupuesto_category_id.type == 'servicio' if order.presupuesto_category_id else False
    
    # Método para convertir presupuesto en pedido u orden de servicio cuando sea necesario
    # Por implementar en el futuro
    def convert_to_order(self):
        self.ensure_one()
        # Esta función sería implementada más adelante para la conversión a pedido o servicio
