from odoo import models, fields, api
from datetime import timedelta

class PropertyType(models.Model):

    _name = 'estate.property.tag'
    _description = 'Tags para propiedades'

    name = fields.Char('Nombre', required=True)

    property_ids = fields.Many2many('estate.property', string='Propiedades relacionadas')

class PropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = 'Oferta de propiedad'

    property_id = fields.Many2one('estate.property', string='Propiedad', required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    price = fields.Float('Precio', required=True)
    status = fields.Selection([
        ('accepted', 'Aceptado'),
        ('refused', 'Rechazado'),
        ('pending', 'Pendiente'),
    ], string='Estado', default='pending', required=True)
    create_date = fields.Datetime('Fecha de creación', default=fields.Datetime.now, readonly=True)
    #tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    #tag_count = fields.Integer('Número de tags', compute='_compute_tag_count')

    validity2 = fields.Integer('Validez (días)', default=7)
    date_deadline = fields.Date(
        string='Fecha límite',
        compute='_compute_deadline',
        inverse='_inverse_deadline',
        store=True
    )
    
    @api.depends('create_date', 'validity2')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity2)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity2)
    
    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.validity2 = (record.date_deadline - create_date).days

    def action_accept(self):
        self.status = 'accepted'

    def action_refuse(self):
        self.status = 'refused'

    def action_pending(self):
        self.status = 'pending'

    #def _compute_tag_count(self):
    #    for record in self:
    #        record.tag_count = len(record.tag_ids)