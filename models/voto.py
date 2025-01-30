from odoo import models, fields

class Voto(models.Model):
    _name = 'uniacme.voto'
    _description = 'Registro de Votos'

    identificacion = fields.Char(string="Cédula")
    estudiante_id = fields.Many2one('res.partner', string="Estudiante", domain="[('es_estudiante', '=', True)]")
    proceso_votacion_id = fields.Many2one('uniacme.proceso.votacion', string="Proceso de Votación", ondelete='cascade')
    candidato_id = fields.Many2one('res.partner', string="Candidato", required=True, domain="[('es_candidato', '=', True)]")
    fecha_voto = fields.Datetime(string="Fecha de Voto", default=fields.Datetime.now, readonly=True)
    sede_id = fields.Many2one('uniacme.sede', related='proceso_votacion_id.sede_id', store=True, string="Sede")


