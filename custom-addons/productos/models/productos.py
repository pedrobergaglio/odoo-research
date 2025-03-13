from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductoCategoria(models.Model):
    _name = 'productos.categoria'
    _description = 'Categoría de Producto'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)
    description = fields.Text('Descripción')
    parent_id = fields.Many2one('productos.categoria', string='Categoría Padre')
    child_ids = fields.One2many('productos.categoria', 'parent_id', string='Subcategorías')
    complete_name = fields.Char('Nombre Completo', compute='_compute_complete_name', store=True)
    product_count = fields.Integer('Cantidad de Productos', compute='_compute_product_count')
    
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = f'{category.parent_id.complete_name} / {category.name}'
            else:
                category.complete_name = category.name
    
    def _compute_product_count(self):
        for category in self:
            category.product_count = self.env['productos.producto'].search_count([
                ('categoria_id', '=', category.id)
            ])

class Producto(models.Model):
    _name = 'productos.producto'
    _description = 'Producto Personalizado'
    
    name = fields.Char('Nombre', required=True)
    reference = fields.Char('Referencia/ID', required=True)
    categoria_id = fields.Many2one('productos.categoria', string='Categoría', required=True)
    imagen = fields.Binary('Imagen del Producto')
    precio = fields.Float('Precio (Con IVA)', required=True)
    tasa_iva = fields.Float('Tasa de IVA (%)', default=15.0)
    precio_sin_iva = fields.Float('Precio (Sin IVA)', compute='_compute_precio_sin_iva', store=True)
    stock = fields.Float('Stock (Cantidad)', default=0.0)
    valor_stock = fields.Float('Valor del Stock', compute='_compute_valor_stock', store=True)
    activo = fields.Boolean('Activo', default=True)
    descripcion = fields.Text('Descripción')
    
    @api.depends('precio', 'tasa_iva')
    def _compute_precio_sin_iva(self):
        for producto in self:
            if producto.tasa_iva:
                producto.precio_sin_iva = producto.precio / (1 + (producto.tasa_iva / 100))
            else:
                producto.precio_sin_iva = producto.precio
    
    @api.depends('precio', 'stock')
    def _compute_valor_stock(self):
        for producto in self:
            producto.valor_stock = producto.precio * producto.stock
    
    @api.constrains('precio')
    def _check_precio(self):
        for producto in self:
            if producto.precio < 0:
                raise ValidationError("El precio no puede ser negativo")
    
    @api.constrains('stock')
    def _check_stock(self):
        for producto in self:
            if producto.stock < 0:
                raise ValidationError("El stock no puede ser negativo")
    
    _sql_constraints = [
        ('reference_uniq', 'unique(reference)', 'La referencia del producto debe ser única!')
    ]