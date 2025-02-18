from odoo import fields, models
import json

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    model_ids = fields.Many2many(
        'ir.model', 
        'hide_chatter_model_rel',
        'config_id',
        'model_id',
        string="Models",
        help="Choose the models to hide their chatter"
    )

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()
        # Store as JSON string
        param.set_param('hide_chatter.model_ids', json.dumps(self.model_ids.ids))

    def get_values(self):
        res = super().get_values()
        param = self.env['ir.config_parameter'].sudo()
        model_ids = param.get_param('hide_chatter.model_ids')
        try:
            parsed_ids = json.loads(model_ids) if model_ids else []
            res.update(
                model_ids=[(6, 0, parsed_ids)]
            )
        except:
            res.update(model_ids=False)
        return res
