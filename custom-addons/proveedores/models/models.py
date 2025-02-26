from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    # Método para establecer valores predeterminados al crear desde la app Proveedores
    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        # Si se crea desde nuestra acción de proveedores, establecer como proveedor por defecto
        context = self.env.context
        if context.get('search_default_suppliers'):
            res['supplier_rank'] = 1
            res['partner_type'] = 'supplier'
        return res