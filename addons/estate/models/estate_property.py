from odoo import models, fields, api
from datetime import timedelta

class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = 'Real Estate Property'

    def _default_date_availability(self):
        return fields.Date.today() + timedelta(days=90)
    
    @api.depends('bedrooms', 'garden_area')
    def _compute_living_area(self):
        for record in self:
            record.living_area = record.bedrooms * 15 + record.garden_area

    name = fields.Char('Nombre', required=True)
    description = fields.Text('Descripción')
    date_availability = fields.Date('Disponible desde', copy=False, default=_default_date_availability)
    expected_price = fields.Float('Precio esperado', required=True)
    selling_price = fields.Float('Precio de venta', readonly=True, copy=False)
    bedrooms = fields.Integer('Habitaciones', default=2)
    living_area = fields.Integer(
        'Área habitable', 
        store=True, 
        compute='_compute_living_area'  # Remove required=True
    )
    facades = fields.Integer('Fachadas')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Jardín')
    garden_area = fields.Integer('Área del jardín')
    garden_orientation = fields.Selection(
        [('north', 'Norte'),
         ('south', 'Sur'),
         ('east', 'Este'),
         ('west', 'Oeste')],
        string='Orientación del jardín'
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'Nuevo'),
        ('offer_received', 'Oferta recibida'),
        ('offer_accepted', 'Oferta aceptada'),
        ('sold', 'Vendido'),
        ('canceled', 'Cancelado'),
    ], string='Estado', default='new', copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Tipo de propiedad')
    buyer_id = fields.Many2one('res.partner', string='Comprador')
    seller_id = fields.Many2one('res.users', string='Vendedor', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Ofertas')
    #offer_count = fields.Integer('Número de ofertas', compute='_compute_offer_count')

    total_area = fields.Integer('Área total', store=True, required=True, compute='_compute_total_area')
    best_offer_id = fields.Float(
        string='Mejor oferta',
        compute='_compute_best_offer_id',
        store=True
    )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == False:
            self.garden_area = 0
            self.garden_orientation = None
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'



    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids', 'offer_ids.price')
    def _compute_best_offer_id(self):
        for record in self:
            best_offer = record.offer_ids.filtered(lambda o: o.price)
            record.best_offer_id = max(best_offer.mapped('price'), default=0.0)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)