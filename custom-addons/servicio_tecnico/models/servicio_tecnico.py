from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ServicioTecnico(models.Model):
    _name = 'servicio.servicio'
    _description = 'Servicio Técnico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Número de Servicio', required=True, copy=False, readonly=True, 
                       default=lambda self: self.env['ir.sequence'].next_by_code('servicio.servicio'))
    
    presupuesto_id = fields.Many2one('presupuesto.presupuesto', string='Presupuesto Relacionado')
    
    # Campos del parent presupuesto
    partner_id = fields.Many2one(related='presupuesto_id.partner_id', string='Cliente', store=True, readonly=True)
    date = fields.Date(related='presupuesto_id.date', string='Fecha de Presupuesto', store=True, readonly=True)
    date_servicio = fields.Date('Fecha de Servicio', default=fields.Date.today, required=True)
    payment_method_id = fields.Many2one(related='presupuesto_id.payment_method_id', string='Método de Pago', store=True)
    
    state = fields.Selection([
        ('confirmado', 'Confirmado'),
        ('en_proceso', 'En Proceso'),
        ('terminado', 'Terminado'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='confirmado', tracking=True)
    
    # Líneas de servicio (heredadas del presupuesto)
    line_ids = fields.One2many('servicio.line', 'servicio_id', string='Líneas de Servicio')
    
    amount_untaxed = fields.Float(string='Base Imponible', compute='_compute_amount', store=True, readonly=True)
    amount_tax = fields.Float(string='IVA', compute='_compute_amount', store=True, readonly=True)
    amount_total = fields.Float(string='Total', compute='_compute_amount', store=True, readonly=True)
    
    fecha_entrega_estimada = fields.Date('Fecha de Entrega Estimada')
    direccion_entrega = fields.Text('Dirección de Entrega')
    
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Moneda', related='company_id.currency_id')
    
    @api.depends('line_ids.price_subtotal', 'line_ids.price_tax')
    def _compute_amount(self):
        for servicio in self:
            amount_untaxed = sum(line.price_subtotal for line in servicio.line_ids)
            amount_tax = sum(line.price_tax for line in servicio.line_ids)
            servicio.amount_untaxed = amount_untaxed
            servicio.amount_tax = amount_tax
            servicio.amount_total = amount_untaxed + amount_tax
    
    @api.model
    def create(self, vals):
        servicio = super(ServicioTecnico, self).create(vals)
        if servicio.presupuesto_id and servicio.presupuesto_id.state == 'presupuesto_servicio':
            servicio.presupuesto_id.write({'state': 'en_proceso'})
        
        for presupuesto_line in servicio.presupuesto_id.line_ids:
            if not presupuesto_line.product_id.exists():  
                _logger.warning(f"Producto con ID {presupuesto_line.product_id.id} no encontrado, omitiendo línea.")
                continue
            self.env['servicio.line'].create({
                'servicio_id': servicio.id,
                'product_id': presupuesto_line.product_id.id,
                'name': presupuesto_line.name,
                'quantity': presupuesto_line.quantity,
                'price_unit': presupuesto_line.price_unit,
            })
        return servicio
    
    def action_en_proceso(self):
        self.write({'state': 'en_proceso'})
    
    def action_terminar(self):
        self.write({'state': 'terminado'})
        if self.presupuesto_id:
            self.presupuesto_id.write({'state': 'finalizado'})
    
    def action_cancelar(self):
        self.write({'state': 'cancelado'})
        if self.presupuesto_id:
            self.presupuesto_id.write({'state': 'cancelado'})

class ServicioTecnicoLine(models.Model):
    _name = 'servicio.line'
    _description = 'Línea de Servicio Técnico'
    
    servicio_id = fields.Many2one('servicio.servicio', string='Servicio', required=True, ondelete='cascade')
    product_id = fields.Many2one('productos.producto', string='Producto', required=True, ondelete='cascade')
    name = fields.Char('Descripción', required=True)
    quantity = fields.Float('Cantidad', default=1.0, required=True)
    price_unit = fields.Float('Precio Unitario', required=True)
    
    price_subtotal = fields.Float('Subtotal', compute='_compute_price', store=True)
    price_tax = fields.Float('Impuestos', compute='_compute_price', store=True)
    price_total = fields.Float('Total', compute='_compute_price', store=True)
    
    currency_id = fields.Many2one(related='servicio_id.currency_id', string='Moneda')
    state = fields.Selection(related='servicio_id.state', string='Estado')
    
    @api.depends('quantity', 'price_unit', 'product_id.tasa_iva')
    def _compute_price(self):
        for line in self:
            subtotal = line.quantity * line.price_unit
            if line.product_id and line.product_id.tasa_iva:
                tax_rate = line.product_id.tasa_iva / 100
                tax_amount = subtotal * tax_rate
            else:
                tax_amount = 0.0
            line.price_subtotal = subtotal
            line.price_tax = tax_amount
            line.price_total = subtotal + tax_amount
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.precio