from odoo import models, fields, api

class CustomClient(models.Model):
    _name = 'custom.client'
    _description = 'Custom Client'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre', required=True, index=True, tracking=True)
    email = fields.Char('Correo Electrónico')
    phone = fields.Char('Teléfono')
    mobile = fields.Char('Móvil')
    website = fields.Char('Sitio Web')
    street = fields.Char('Calle')
    street2 = fields.Char('Calle 2')
    city = fields.Char('Ciudad')
    state_id = fields.Many2one('res.country.state', 'Estado')
    country_id = fields.Many2one('res.country', 'País')
    zip = fields.Char('Código Postal')
    category = fields.Selection([
        ('client', 'Cliente'),
        ('supplier', 'Proveedor'),
        ('both', 'Ambos')
    ], string='Categoría', default='client', required=True, tracking=True)
    image = fields.Binary('Foto', attachment=True)
    active = fields.Boolean('Activo', default=True)

    # Relaciones con Pedidos y Servicios
    pedido_ids = fields.One2many('pedido.pedido', 'partner_id', string='Pedidos Activos', domain=[('state', 'in', ['confirmado', 'en_preparacion', 'listo_para_entrega'])])
    servicio_ids = fields.One2many('servicio.servicio', 'partner_id', string='Servicios Activos', domain=[('state', 'in', ['confirmado', 'en_proceso'])])
    total_amount_pedidos = fields.Float('Total Pedidos', compute='_compute_total_amounts')
    total_amount_servicios = fields.Float('Total Servicios', compute='_compute_total_amounts')

    # Campos relacionados para los Pedidos
    pedido_name = fields.Char(related='pedido_ids.name', string='Nombre del Pedido', readonly=True)
    pedido_date = fields.Date(related='pedido_ids.date', string='Fecha del Pedido', readonly=True)
    pedido_amount_total = fields.Float(related='pedido_ids.amount_total', string='Total del Pedido', readonly=True)
    pedido_state = fields.Selection(related='pedido_ids.state', string='Estado del Pedido', readonly=True)

    # Campos relacionados para los Servicios
    servicio_name = fields.Char(related='servicio_ids.name', string='Nombre del Servicio', readonly=True)
    servicio_date_servicio = fields.Date(related='servicio_ids.date_servicio', string='Fecha del Servicio', readonly=True)
    servicio_amount_total = fields.Float(related='servicio_ids.amount_total', string='Total del Servicio', readonly=True)
    servicio_state = fields.Selection(related='servicio_ids.state', string='Estado del Servicio', readonly=True)

    @api.depends('pedido_ids.amount_total', 'servicio_ids.amount_total')
    def _compute_total_amounts(self):
        for client in self:
            client.total_amount_pedidos = sum(p.amount_total for p in client.pedido_ids)
            client.total_amount_servicios = sum(s.amount_total for s in client.servicio_ids)

    