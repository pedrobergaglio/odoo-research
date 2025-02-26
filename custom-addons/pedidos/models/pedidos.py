from odoo import models, fields, api

class SaleOrderType(models.Model):
    _name = 'sale.order.type'
    _description = 'Tipo de Orden de Venta'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)
    description = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_type_id = fields.Many2one('sale.order.type', string='Tipo de Orden', 
                                 tracking=True,
                                 help="Identifica el tipo de orden")
    is_pedido = fields.Boolean('Es Pedido', compute='_compute_is_pedido', store=True)

    @api.depends('order_type_id')
    def _compute_is_pedido(self):
        pedido_type = self.env.ref('pedidos.sale_order_type_pedido', False)
        for order in self:
            if pedido_type and order.order_type_id:
                order.is_pedido = order.order_type_id.id == pedido_type.id
            else:
                order.is_pedido = False