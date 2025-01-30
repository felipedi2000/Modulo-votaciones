from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UniacmeEstudiante(models.Model):
    _name= 'res.partner'
    _inherit = 'res.partner'

    # Información adicional de los estudiantes
    carrera = fields.Selection([
        ('ingenieria_sistemas', 'Ingeniería de Sistemas'),
        ('ingenieria_electronica', 'Ingeniería Electrónica'),
        ('administracion', 'Administración de Empresas'),
        ('psicologia', 'Psicología'),
        ('medicina', 'Medicina'),
    ], string="Carrera", required=True)

    es_estudiante = fields.Boolean()
    es_candidato = fields.Boolean()
    sede_id = fields.Many2one('uniacme.sede', string="Sede")
    is_company = fields.Boolean(default=True)
    ha_votado = fields.Boolean(string='Ha Votado', compute='_compute_ha_votado', store=True)
    voto_ids = fields.One2many('uniacme.voto', 'estudiante_id', string="Votos")
    
    
    # Validación para no permitir duplicidad de identificación
    @api.constrains('vat')
    def _check_identificacion_unica(self):
        for record in self:
            estudiantes_con_mismo_id = self.search([('vat', '=', record.vat)])
            if len(estudiantes_con_mismo_id) > 1:
                raise ValidationError("El número de identificación ya está registrado en el sistema.")

    @api.depends('voto_ids')
    def _compute_ha_votado(self):
        for record in self:
            record.ha_votado = bool(record.voto_ids)