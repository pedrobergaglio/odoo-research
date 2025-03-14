# -*- coding: utf-8 -*-

from odoo import models, fields, api
import uuid
import datetime

class CajaMovimiento(models.Model):
    _name = 'caja.movimiento'
    _description = 'Movimientos de Caja'
    _order = 'fecha desc, id desc'

    def _generate_unique_id(self):
        return str(uuid.uuid4())[:8]

    id_movimiento = fields.Char(string='ID Movimiento', default=_generate_unique_id, readonly=True)
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now, required=True)
    categoria = fields.Selection([
        ('cliente', 'Cliente'),
        ('deposito', 'Depósito'),
        ('empleado', 'Empleado'),
        ('proveedor', 'Proveedor'),
        ('otro', 'Otro')
    ], string='Categoría', required=True)
    metodo_pago = fields.Selection([
        ('dolares', 'Dólares'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria')
    ], string='Método de Pago', required=True)
    monto = fields.Float(string='Monto', required=True)
    aclaracion = fields.Text(string='Aclaración')
    
    # Campo computado para mostrar el saldo actualizado
    saldo_caja = fields.Float(string='Saldo en Caja', compute='_compute_saldo_caja', store=False)

    @api.depends('monto')
    def _compute_saldo_caja(self):
        for record in self:
            # Buscar todos los movimientos anteriores o iguales a la fecha actual
            movimientos = self.env['caja.movimiento'].search([
                ('fecha', '<=', record.fecha)
            ])
            record.saldo_caja = sum(movimiento.monto for movimiento in movimientos)