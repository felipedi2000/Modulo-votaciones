from odoo import models, fields, exceptions
from datetime import datetime, timedelta, timezone
import re

class VotoWizard(models.TransientModel):
    _name = 'voto.wizard'
    _description = 'Formulario de Votación'

    identificacion = fields.Char(string="Cédula", required=True)
    estudiante_id = fields.Many2one('res.partner', string="Estudiante", domain="[('es_estudiante', '=', True)]", readonly=True)
    proceso_votacion_id = fields.Many2one('uniacme.proceso.votacion', string="Proceso de Votación", required=True)
    candidato_id = fields.Many2one('res.partner', string="Candidato", required=True, domain="[('es_candidato', '=', True)]")
    fecha_voto = fields.Datetime(string="Fecha de Voto", default=fields.Datetime.now, readonly=True)
    sede_id = fields.Many2one('uniacme.sede', related='proceso_votacion_id.sede_id', store=True, string="Sede")

    def confirmar_voto(self):
        for record in self:
            estudiante = self.env['res.partner'].search([('vat', '=', record.identificacion)], limit=1)
            
            if not estudiante:
                raise exceptions.ValidationError("Estudiante no encontrado")
            
            if self.env['uniacme.voto'].search([
                ('estudiante_id', '=', estudiante.id),
                ('proceso_votacion_id', '=', record.proceso_votacion_id.id),
            ], limit=1):
                raise exceptions.ValidationError("El estudiante ya ha votado en este proceso de votación.")

            # Obtener la sede del estudiante y su zona horaria
            sede_estudiante = estudiante.sede_id
            if not sede_estudiante:
                raise exceptions.ValidationError("Sede no asignada al estudiante.")

            timezone_estudiante = sede_estudiante.timezone
            # Obtener la zona horaria de la sede del proceso de votación
            sede_proceso_votacion = record.proceso_votacion_id.sede_id
            timezone_sede = sede_proceso_votacion.timezone
            if not timezone_sede:
                raise exceptions.ValidationError("Zona horaria no asignada a la sede.")

            match_sede  = re.search(r'(?:GMT)([+-]\d+)', timezone_sede)
            if not match_sede :
                raise exceptions.ValidationError("Formato de zona horaria no válido.")
            offset_horas_sede = int(match_sede .group(1))

            match_estudiante = re.search(r'(?:GMT)([+-]\d+)', timezone_estudiante)
            if not match_estudiante:
                raise exceptions.ValidationError("Formato de zona horaria no válido para el estudiante.")
            offset_horas_estudiante = int(match_estudiante.group(1))

            hora_actual_ajustada_sede = datetime.now(timezone.utc) + timedelta(hours=offset_horas_sede)

            # Convertir fecha_hora_inicio_sede y fecha_hora_limite_estudiante a objetos con zona horaria
            fecha_hora_inicio_sede = record.proceso_votacion_id.periodo_inicio + timedelta(hours=offset_horas_sede)
            fecha_hora_inicio_sede = fecha_hora_inicio_sede.replace(tzinfo=timezone.utc)  # Hacerlo aware si es necesario

            fecha_hora_limite_sede = record.proceso_votacion_id.periodo_fin + timedelta(hours=offset_horas_sede)
            fecha_hora_limite_sede = fecha_hora_limite_sede.replace(tzinfo=timezone.utc)  # Hacerlo aware si es necesario

            # Ajuste según la zona horaria del estudiante (ajustamos a la zona horaria del estudiante)
            fecha_hora_limite_estudiante = fecha_hora_limite_sede - timedelta(hours=(offset_horas_estudiante - offset_horas_sede))
            fecha_hora_limite_estudiante = fecha_hora_limite_estudiante.replace(tzinfo=timezone.utc)  # Hacerlo aware si es necesario

            if not (fecha_hora_inicio_sede <= hora_actual_ajustada_sede <= fecha_hora_limite_estudiante):
                raise exceptions.ValidationError(
                    f"❌ La fecha actual ({hora_actual_ajustada_sede.strftime('%Y-%m-%d %H:%M:%S')}) "
                    f"no está dentro del rango permitido para el proceso de votación. "
                    f"Rango: {fecha_hora_inicio_sede.strftime('%Y-%m-%d %H:%M:%S')} - {fecha_hora_limite_estudiante.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            
            voto_data = {
                'estudiante_id': estudiante.id,
                'proceso_votacion_id': record.proceso_votacion_id.id,
                'fecha_voto': datetime.now(),
                'identificacion': record.identificacion,
                'sede_id': sede_estudiante.id,
                'candidato_id': record.candidato_id.id,
            }

            self.env['uniacme.voto'].create(voto_data)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
