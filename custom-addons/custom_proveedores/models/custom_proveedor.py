from odoo import models, fields, api

class CustomProveedor(models.Model):
    _name = 'custom.proveedor'
    _description = 'Custom Proveedor'
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
        ('supplier', 'Proveedor'),
        ('both', 'Ambos')
    ], string='Categoría', default='supplier', required=True, tracking=True)
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
        for proveedor in self:
            proveedor.total_amount_pedidos = sum(p.amount_total for p in proveedor.pedido_ids)
            proveedor.total_amount_servicios = sum(s.amount_total for s in proveedor.servicio_ids)

    @api.model
    def create(self, vals):
        # Si está en contexto de sincronización, no crear más registros
        if self.env.context.get('skip_sync'):
            return super(CustomProveedor, self).create(vals)

        # Crear el registro en custom.proveedor
        proveedor = super(CustomProveedor, self).create(vals)

        # Si la categoría es "ambos", crear un registro en custom.client con skip_sync
        if proveedor.category == 'both':
            client_vals = {
                'name': proveedor.name,
                'email': proveedor.email,
                'phone': proveedor.phone,
                'mobile': proveedor.mobile,
                'website': proveedor.website,
                'street': proveedor.street,
                'street2': proveedor.street2,
                'city': proveedor.city,
                'state_id': proveedor.state_id.id,
                'country_id': proveedor.country_id.id,
                'zip': proveedor.zip,
                'category': 'both',
                'image': proveedor.image,
                'active': proveedor.active,
            }
            self.with_context(skip_sync=True).env['custom.client'].create(client_vals)

        return proveedor

    def write(self, vals):
        # Actualizar el registro en custom.proveedor
        result = super(CustomProveedor, self).write(vals)

        # Si la categoría es "ambos", actualizar o crear en custom.client
        for proveedor in self:
            if proveedor.category == 'both' and not self.env.context.get('skip_sync'):
                client = self.env['custom.client'].search([('name', '=', proveedor.name), ('category', '=', 'both')], limit=1)
                client_vals = {
                    'name': proveedor.name,
                    'email': proveedor.email,
                    'phone': proveedor.phone,
                    'mobile': proveedor.mobile,
                    'website': proveedor.website,
                    'street': proveedor.street,
                    'street2': proveedor.street2,
                    'city': proveedor.city,
                    'state_id': proveedor.state_id.id,
                    'country_id': proveedor.country_id.id,
                    'zip': proveedor.zip,
                    'category': 'both',
                    'image': proveedor.image,
                    'active': proveedor.active,
                }
                if client:
                    client.with_context(skip_sync=True).write(client_vals)
                else:
                    self.with_context(skip_sync=True).env['custom.client'].create(client_vals)

        return result

    def action_view_pedido(self, pedido_id):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pedido.pedido',
            'res_id': pedido_id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_servicio(self, servicio_id):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'servicio.servicio',
            'res_id': servicio_id,
            'view_mode': 'form',
            'target': 'current',
        }