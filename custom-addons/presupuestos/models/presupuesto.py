from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class PresupuestoCategoria(models.Model):
    _name = 'presupuesto.categoria'
    _description = 'Categoría de Presupuesto'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)

class Presupuesto(models.Model):
    _name = 'presupuesto.presupuesto'
    _description = 'Presupuesto'
    _order = 'date desc, id desc'

    name = fields.Char('Número de Presupuesto', required=True, copy=False, readonly=True, 
                      default=lambda self: self.env['ir.sequence'].next_by_code('presupuesto.presupuesto'))
    
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date = fields.Date('Fecha', default=fields.Date.today, required=True, tracking=True)
    
    payment_method_id = fields.Many2one('account.payment.method', string='Método de Pago')
    
    categoria_id = fields.Many2one('presupuesto.categoria', string='Categoría', required=True, tracking=True,
                                   domain="[('code', 'in', ['pedido', 'servicio'])]")
    categoria_code = fields.Char(related='categoria_id.code', string='Código de Categoría', store=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('presupuestado', 'Presupuestado'),
        ('presupuesto_pedido', 'Presupuesto Pedido'),
        ('presupuesto_servicio', 'Presupuesto Servicio'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado')
    ], string='Estado', default='draft', tracking=True)
    
    # Líneas de productos
    line_ids = fields.One2many('presupuesto.line', 'presupuesto_id', string='Líneas de Presupuesto')

    amount_untaxed = fields.Float('Base Imponible', compute='_compute_amounts', store=True)
    amount_tax = fields.Float('IVA', compute='_compute_amounts', store=True)
    amount_total = fields.Float('Total', compute='_compute_amounts', store=True)
    
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Moneda', related='company_id.currency_id')
    
    #Creacion de pedidos en pedidos.pedidos
    def write(self, vals):
        if 'state' in vals and vals['state'] == 'presupuesto_pedido':
            for record in self:
                # Solo crear el pedido si el estado anterior no era 'presupuesto_pedido'
                if record.state != 'presupuesto_pedido':
                    self._create_pedido(record)
        return super(Presupuesto, self).write(vals)

    def _create_pedido(self, presupuesto):
        pedido = self.env['pedido.pedido'].create({
            'name': f"Pedido de {presupuesto.name}",
            'partner_id': presupuesto.partner_id.id,
            'date': fields.Date.today(),
            'presupuesto_id': presupuesto.id,
            'state': 'confirmado',
        })
        return pedido

    #Creacion de servicio en servicio.servicio
    def write(self, vals):
        if 'state' in vals and vals['state'] == 'presupuesto_servicio':
            for record in self:
                # Solo crear el pedido si el estado anterior no era 'presupuesto_servicio'
                if record.state != 'presupuesto_servicio':
                    self._create_servicio(record)
        return super(Presupuesto, self).write(vals)

    def _create_servicio(self, presupuesto):
        servicio = self.env['servicio.servicio'].create({
            'name': f"Servicio de {presupuesto.name}",
            'partner_id': presupuesto.partner_id.id,
            'date': fields.Date.today(),
            'presupuesto_id': presupuesto.id,
            'state': 'confirmado',
        })
        return servicio

    @api.depends('line_ids.price_subtotal', 'line_ids.price_tax')
    def _compute_amounts(self):
        for presupuesto in self:
            amount_untaxed = sum(line.price_subtotal for line in presupuesto.line_ids)
            amount_tax = sum(line.price_tax for line in presupuesto.line_ids)
            presupuesto.amount_untaxed = amount_untaxed
            presupuesto.amount_tax = amount_tax
            presupuesto.amount_total = amount_untaxed + amount_tax
    def action_presupuestar(self):
        self.write({'state': 'presupuestado'})
    
    def action_confirmar_pedido(self):
        for rec in self:
            if rec.categoria_code != 'pedido':
                raise ValidationError('Solo presupuestos de categoría "Pedido" pueden ser confirmados como pedidos.')
            rec.write({'state': 'presupuesto_pedido'})
    
    def action_confirmar_servicio(self):
        for rec in self:
            if rec.categoria_code != 'servicio':
                raise ValidationError('Solo presupuestos de categoría "Servicio" pueden ser confirmados como servicios.')
            rec.write({'state': 'presupuesto_servicio'})
    
    def action_en_proceso(self):
        self.write({'state': 'en_proceso'})
    
    def action_finalizar(self):
        self.write({'state': 'finalizado'})
    
    def action_cancelar(self):
        self.write({'state': 'cancelado'})
    
    def action_draft(self):
        self.write({'state': 'draft'})

class PresupuestoLine(models.Model):
    _name = 'presupuesto.line'
    _description = 'Línea de Presupuesto'
    
    presupuesto_id = fields.Many2one('presupuesto.presupuesto', string='Presupuesto', required=True, ondelete='cascade')
    product_id = fields.Many2one('productos.producto', string='Producto', required=True)
    name = fields.Char('Descripción', required=True)
    quantity = fields.Float('Cantidad', default=1.0, required=True)
    price_unit = fields.Float('Precio Unitario', required=True)
    
    price_subtotal = fields.Float('Subtotal', compute='_compute_price', store=True)
    price_tax = fields.Float('Impuestos', compute='_compute_price', store=True)
    price_total = fields.Float('Total', compute='_compute_price', store=True)
    
    currency_id = fields.Many2one(related='presupuesto_id.currency_id', string='Moneda')
    state = fields.Selection(related='presupuesto_id.state', string='Estado')
    
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