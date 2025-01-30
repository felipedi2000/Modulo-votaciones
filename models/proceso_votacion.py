from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UniacmeProcesoVotacion(models.Model):
    _name = 'uniacme.proceso.votacion'
    _description = 'Proceso de Votación'

    name = fields.Char(string="Descripción", required=True)
    periodo_inicio = fields.Datetime(string="Fecha y Hora de Inicio", required=True)
    periodo_fin = fields.Datetime(string="Fecha y Hora de Fin", required=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('cerrada', 'Cerrada')
    ], default='borrador', string="Estado")
    candidatos_ids = fields.Many2many('res.partner', domain=[('es_candidato', '=', True)], string="Candidatos")
    votos = fields.One2many('uniacme.voto', 'proceso_votacion_id', string="Votos")
    sede_id = fields.Many2one('uniacme.sede', string="Sede")
    

    @api.constrains('periodo_inicio', 'periodo_fin')
    def _check_periodo_votacion(self):
        for record in self:
            if record.periodo_inicio >= record.periodo_fin:
                raise ValidationError("La fecha y hora de inicio debe ser anterior a la fecha y hora de fin.")
    
    def comenzar_proceso_votacion(self):
        for record in self:
            if record.estado == 'borrador':
                record.write({'estado': 'en_proceso'})
            else:
                raise ValidationError("La votación ya está en proceso o cerrada.")
