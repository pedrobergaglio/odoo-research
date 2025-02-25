from odoo import models, fields

class PropertyType(models.Model):

    _name = 'estate.property.type'
    _description = 'Tipo de propiedad'

    name = fields.Char('Nombre', required=True)