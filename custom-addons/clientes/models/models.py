from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    partner_type = fields.Selection([
        ('customer', 'Cliente'),
        ('supplier', 'Proveedor'),
        ('both', 'Ambos')
    ], string='Tipo de Contacto', compute='_compute_partner_type', store=True, readonly=False)
    
    @api.depends('customer_rank', 'supplier_rank')
    def _compute_partner_type(self):
        for partner in self:
            if partner.customer_rank > 0 and partner.supplier_rank > 0:
                partner.partner_type = 'both'
            elif partner.customer_rank > 0:
                partner.partner_type = 'customer'
            elif partner.supplier_rank > 0:
                partner.partner_type = 'supplier'
            else:
                partner.partner_type = False
    
    @api.onchange('partner_type')
    def _onchange_partner_type(self):
        for partner in self:
            if partner.partner_type == 'customer':
                partner.customer_rank = 1
                partner.supplier_rank = 0
            elif partner.partner_type == 'supplier':
                partner.customer_rank = 0
                partner.supplier_rank = 1
            elif partner.partner_type == 'both':
                partner.customer_rank = 1
                partner.supplier_rank = 1
            else:
                partner.customer_rank = 0
                partner.supplier_rank = 0
    
    # Método para establecer valores predeterminados al crear desde la app Clientes
    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        # Si se crea desde nuestra acción de clientes, establecer como cliente por defecto
        context = self.env.context
        if context.get('search_default_customers'):
            res['customer_rank'] = 1
            res['partner_type'] = 'customer'
        return res
    
    def update_partner_type(self):
        """Forzar la actualización del tipo de contacto"""
        self.ensure_one()
        if self.partner_type == 'customer':
            self.write({'customer_rank': 1, 'supplier_rank': 0})
        elif self.partner_type == 'supplier':
            self.write({'customer_rank': 0, 'supplier_rank': 1})
        elif self.partner_type == 'both':
            self.write({'customer_rank': 1, 'supplier_rank': 1})
        else:
            self.write({'customer_rank': 0, 'supplier_rank': 0})
        
        # Retornar una acción para refrescar la vista
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }