from odoo import models, fields, api

class CustomClient(models.Model):
    _name = 'custom.client'
    _description = 'Custom Client'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre', required=True)
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
        ('both', 'Ambos')
    ], string='Categoría', default='client', required=True, tracking=True)
    image = fields.Binary('Foto', attachment=True)
    active = fields.Boolean('Activo', default=True)

    pedido_ids = fields.One2many('pedido.pedido', 'partner_id', string='Pedidos Activos', domain=[('state', 'in', ['confirmado', 'en_preparacion', 'listo_para_entrega'])])
    servicio_ids = fields.One2many('servicio.servicio', 'partner_id', string='Servicios Activos', domain=[('state', 'in', ['confirmado', 'en_proceso'])])
    total_amount_pedidos = fields.Float('Total Pedidos', compute='_compute_total_amounts')
    total_amount_servicios = fields.Float('Total Servicios', compute='_compute_total_amounts')

    pedido_name = fields.Char(related='pedido_ids.name', string='Nombre del Pedido', readonly=True)
    pedido_date = fields.Date(related='pedido_ids.date', string='Fecha del Pedido', readonly=True)
    pedido_amount_total = fields.Float(related='pedido_ids.amount_total', string='Total del Pedido', readonly=True)
    pedido_state = fields.Selection(related='pedido_ids.state', string='Estado del Pedido', readonly=True)

    servicio_name = fields.Char(related='servicio_ids.name', string='Nombre del Servicio', readonly=True)
    servicio_date_servicio = fields.Date(related='servicio_ids.date_servicio', string='Fecha del Servicio', readonly=True)
    servicio_amount_total = fields.Float(related='servicio_ids.amount_total', string='Total del Servicio', readonly=True)
    servicio_state = fields.Selection(related='servicio_ids.state', string='Estado del Servicio', readonly=True)

    @api.depends('pedido_ids.amount_total', 'servicio_ids.amount_total')
    def _compute_total_amounts(self):
        for client in self:
            client.total_amount_pedidos = sum(p.amount_total for p in client.pedido_ids)
            client.total_amount_servicios = sum(s.amount_total for s in client.servicio_ids)

    @api.model
    def create(self, vals):
        # Si está en contexto de sincronización, no crear más registros
        if self.env.context.get('skip_sync'):
            return super(CustomClient, self).create(vals)

        # Crear el registro en custom.client
        client = super(CustomClient, self).create(vals)

        # Si la categoría es "ambos", crear un registro en custom.proveedor con skip_sync
        if client.category == 'both':
            proveedor_vals = {
                'name': client.name,
                'email': client.email,
                'phone': client.phone,
                'mobile': client.mobile,
                'website': client.website,
                'street': client.street,
                'street2': client.street2,
                'city': client.city,
                'state_id': client.state_id.id,
                'country_id': client.country_id.id,
                'zip': client.zip,
                'category': 'both',
                'image': client.image,
                'active': client.active,
            }
            self.with_context(skip_sync=True).env['custom.proveedor'].create(proveedor_vals)

        return client

    def write(self, vals):
        # Actualizar el registro en custom.client
        result = super(CustomClient, self).write(vals)

        # Si la categoría es "ambos", actualizar o crear en custom.proveedor
        for client in self:
            if client.category == 'both' and not self.env.context.get('skip_sync'):
                proveedor = self.env['custom.proveedor'].search([('name', '=', client.name), ('category', '=', 'both')], limit=1)
                proveedor_vals = {
                    'name': client.name,
                    'email': client.email,
                    'phone': client.phone,
                    'mobile': client.mobile,
                    'website': client.website,
                    'street': client.street,
                    'street2': client.street2,
                    'city': client.city,
                    'state_id': client.state_id.id,
                    'country_id': client.country_id.id,
                    'zip': client.zip,
                    'category': 'both',
                    'image': client.image,
                    'active': client.active,
                }
                if proveedor:
                    proveedor.with_context(skip_sync=True).write(proveedor_vals)
                else:
                    self.with_context(skip_sync=True).env['custom.proveedor'].create(proveedor_vals)

        return result