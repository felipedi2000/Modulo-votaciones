from odoo import models, fields, api

class UniacmeSede(models.Model):
    _name = 'uniacme.sede'
    _description = 'Sede de la Universidad'

    name = fields.Char(string="Nombre de la Sede", required=True)
    
    country_id = fields.Selection(
        string='País',
        selection=[
            ('BE', 'Bélgica'),
            ('CO', 'Colombia'),
            ('VE', 'Venezuela'),
            ('AR', 'Argentina'),
        ],
        required=True
    )
    
    timezone = fields.Selection(
        string='Zona Horaria',
        selection=[
            ('GMT+1', 'GMT+1 (Bélgica)'),
            ('GMT-5', 'GMT-5 (Colombia)'),
            ('GMT-4', 'GMT-4 (Venezuela)'),
            ('GMT-3', 'GMT-3 (Argentina)'),
        ],
        help='Zona horaria asignada automáticamente según el país seleccionado.',
        required=False
    )

    @api.onchange('country_id')
    def _onchange_country_id(self):
        country_timezones = {
            'BE': 'GMT+1',  # Bélgica
            'CO': 'GMT-5',  # Colombia
            'VE': 'GMT-4',  # Venezuela
            'AR': 'GMT-3',  # Argentina
        }
        if self.country_id:
            self.timezone = country_timezones.get(self.country_id, 'GMT-0')
        else:
            self.timezone = False