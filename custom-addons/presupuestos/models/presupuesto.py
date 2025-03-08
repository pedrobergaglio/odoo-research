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
    
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True, tracking=True)
    address = fields.Char(related='partner_id.contact_address', string='Dirección', readonly=True)
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
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)
    
    # Líneas de productos
    line_ids = fields.One2many('presupuesto.line', 'presupuesto_id', string='Líneas de Presupuesto')

    amount_untaxed = fields.Float('Base Imponible', compute='_compute_amounts', store=True)
    amount_tax = fields.Float('IVA', compute='_compute_amounts', store=True)
    amount_total = fields.Float('Total', compute='_compute_amounts', store=True)
    
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Moneda', related='company_id.currency_id')
    
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
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    name = fields.Char('Descripción', required=True)
    quantity = fields.Float('Cantidad', default=1.0, required=True)
    price_unit = fields.Float('Precio Unitario', required=True)
    tax_id = fields.Many2many('account.tax', string='Impuestos')
    
    price_subtotal = fields.Float('Subtotal', compute='_compute_price', store=True)
    price_tax = fields.Float('Impuestos', compute='_compute_price', store=True)
    price_total = fields.Float('Total', compute='_compute_price', store=True)
    
    currency_id = fields.Many2one(related='presupuesto_id.currency_id', string='Moneda')
    state = fields.Selection(related='presupuesto_id.state', string='Estado')
    
    @api.depends('quantity', 'price_unit', 'tax_id')
    def _compute_price(self):
        for line in self:
            subtotal = line.quantity * line.price_unit
            taxes = line.tax_id.compute_all(line.price_unit, line.presupuesto_id.currency_id, line.quantity, line.product_id, line.presupuesto_id.partner_id)
            line.price_subtotal = taxes['total_excluded']
            line.price_tax = taxes['total_included'] - taxes['total_excluded']
            line.price_total = taxes['total_included']
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.list_price
            self.tax_id = self.product_id.taxes_id