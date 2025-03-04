from odoo import models, fields, api

class ServiceOrderType(models.Model):
    _name = 'service.order.type'
    _description = 'Tipo de Orden de Servicio'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)
    description = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    service_type_id = fields.Many2one('service.order.type', string='Tipo de Servicio', 
                                   tracking=True,
                                   help="Identifica el tipo de servicio técnico")
    is_service = fields.Boolean('Es Servicio Técnico', compute='_compute_is_service', store=True)

    @api.depends('service_type_id')
    def _compute_is_service(self):
        for order in self:
            service_type = self.env.ref('servicio_tecnico.service_order_type_tecnico', False)
            if service_type and order.service_type_id:
                order.is_service = order.service_type_id.id == service_type.id
            else:
                order.is_service = False