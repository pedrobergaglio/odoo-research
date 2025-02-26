from odoo import http
from odoo.http import request

class PriceUpdateController(http.Controller):
    @http.route('/price_update/info', auth='user')
    def price_update_info(self, **kwargs):
        return """
        <html>
            <head>
                <title>Información de Actualización de Precios</title>
            </head>
            <body>
                <h1>Información de Actualización de Precios</h1>
                <p>Esta es una página de información sobre la actualización de precios.</p>
            </body>
        </html>
        """