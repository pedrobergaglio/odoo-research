from odoo import models, fields, api
from odoo.exceptions import UserError

class PriceUpdateWizard(models.TransientModel):
    _name = 'price.update.wizard'
    _description = 'Asistente para actualizar precios por categoría'

    category_id = fields.Many2one('product.category', string='Categoría de Producto', required=True)
    percentage = fields.Float(string='Porcentaje (%)', required=True, help='Porcentaje de cambio en el precio. Positivo para incremento, negativo para descuento.')
    
    def action_update_prices(self):
        if self.percentage == 0:
            raise UserError('El porcentaje no puede ser 0.')
            
        # Buscar todos los productos con la categoría seleccionada
        products = self.env['product.product'].search([('categ_id', '=', self.category_id.id)])
        
        if not products:
            raise UserError(f'No se encontraron productos en la categoría {self.category_id.name}')
            
        # Contador para el mensaje de confirmación
        updated_count = 0
        
        # Actualizar el precio de cada producto
        for product in products:
            if product.lst_price:  # Verificar que el producto tenga un precio
                # Calcular el nuevo precio aplicando el porcentaje
                new_price = product.lst_price * (1 + (self.percentage / 100))
                product.write({'lst_price': new_price})
                updated_count += 1
        
        # Mostrar mensaje de confirmación
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Actualización Completada',
                'message': f'Se actualizaron los precios de {updated_count} productos en la categoría {self.category_id.name} con un {self.percentage}%.',
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }