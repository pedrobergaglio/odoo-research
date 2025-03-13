from odoo import models, fields, api
from odoo.exceptions import UserError

class PriceUpdateWizard(models.TransientModel):
    _name = 'price.update.wizard'
    _description = 'Asistente para actualizar precios por categorías'

    category_ids = fields.Many2many(
        'productos.categoria', 
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
            products = self.env['productos.producto'].search([
                ('categoria_id', 'child_of', category.id)  # Cambiado de categ_id a categoria_id
            ])
            
            # Contador para esta categoría
            category_updated_count = 0
            
            # Actualizar precio de cada producto
            for product in products:
                if product.precio:  # Verificar que el producto tenga un precio (cambiamos lst_price por precio)
                    # Calcular nuevo precio
                    new_price = product.precio * (1 + (self.percentage / 100))
                    
                    # Actualizar precio
                    product.write({'precio': new_price})  # Cambiado de lst_price a precio
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
