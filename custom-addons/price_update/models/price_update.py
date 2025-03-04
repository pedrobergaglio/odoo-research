from odoo import models, fields, api
from odoo.exceptions import UserError

class PriceUpdateWizard(models.TransientModel):
    _name = 'price.update.wizard'
    _description = 'Asistente para actualizar precios por categorías'

    category_ids = fields.Many2many(
        'product.category', 
        string='Categorías de Producto', 
        required=True, 
        help="Selecciona las categorías de productos a actualizar"
    )
    percentage = fields.Float(
        string='Porcentaje (%)', 
        required=True, 
        help='Porcentaje de cambio en el precio. Positivo para incremento, negativo para descuento.'
    )
    
    def action_update_prices(self):
        if self.percentage == 0:
            raise UserError('El porcentaje no puede ser 0.')
        
        if not self.category_ids:
            raise UserError('Debe seleccionar al menos una categoría.')
        
        # Preparar estadísticas
        total_updated_products = 0
        update_details = []
        
        # Iterar sobre cada categoría seleccionada
        for category in self.category_ids:
            # Buscar todos los productos en esta categoría (incluyendo subcategorías)
            products = self.env['product.product'].search([
                ('categ_id', 'child_of', category.id)
            ])
            
            # Contador para esta categoría
            category_updated_count = 0
            
            # Actualizar precio de cada producto
            for product in products:
                if product.lst_price:  # Verificar que el producto tenga un precio
                    # Calcular nuevo precio
                    new_price = product.lst_price * (1 + (self.percentage / 100))
                    
                    # Actualizar precio
                    product.write({'lst_price': new_price})
                    category_updated_count += 1
            
            # Añadir detalles de esta categoría
            update_details.append({
                'category_name': category.name,
                'updated_products': category_updated_count
            })
            
            total_updated_products += category_updated_count
        
        # Preparar mensaje de notificación detallado
        message_lines = [
            "Resumen de Actualización de Precios:",
            f"Porcentaje aplicado: {self.percentage}%",
            f"Total de productos actualizados: {total_updated_products}"
        ]
        
        # Añadir detalles por categoría
        for detail in update_details:
            message_lines.append(
                f"- Categoría {detail['category_name']}: {detail['updated_products']} productos actualizados"
            )
        
        # Mostrar notificación detallada
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Actualización de Precios Completada',
                'message': '\n'.join(message_lines),
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
