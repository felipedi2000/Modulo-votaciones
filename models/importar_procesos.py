from odoo import models, fields,  exceptions
import base64
import re
import csv
import io
from datetime import datetime

class ImportarProcesosWizard(models.TransientModel):
    _name = 'importar.procesos.wizard'
    _description = 'Wizard para Importar Procesos de Votación'

    archivo = fields.Binary(string="Archivo CSV")
    nombre_archivo = fields.Char(string="Nombre del Archivo")

    def importar_procesos(self):
        # Asegurarnos que solo haya un registro de este modelo
        self.ensure_one()

        # Verificamos que se haya subido un archivo
        if not self.archivo:
            raise exceptions.UserError("Por favor, adjunte un archivo CSV.")

        # Decodificamos el archivo CSV subido
        archivo_data = base64.b64decode(self.archivo)
        archivo_csv = io.StringIO(archivo_data.decode('utf-8'))

        lector_csv = csv.reader(archivo_csv)

        # Saltamos la cabecera del archivo
        next(lector_csv)
        # Saltamos la segunda
        next(lector_csv)

        # Leemos las líneas del archivo CSV
        for fila in lector_csv:
            if len(fila) < 4:
                continue  # Saltar filas mal formateadas
            
            # Validar los campos
            nombre = fila[0]
            try:
                periodo_inicio = datetime.strptime(fila[1], '%Y-%m-%d %H:%M:%S')
                periodo_fin = datetime.strptime(fila[2], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise exceptions.UserError(f"Las fechas de la fila '{fila}' no tienen el formato correcto (YYYY-MM-DD HH:MM:SS).")

            sede_nombre = fila[3]

            # Buscar la sede correspondiente
            sede = self.env['uniacme.sede'].search([('name', '=', sede_nombre)], limit=1)
            if not sede:
                raise exceptions.UserError(f"No se encontró la sede '{sede_nombre}' en el sistema.")

            # Crear el proceso de votación
            self.env['uniacme.proceso.votacion'].create({
                'name': nombre,
                'periodo_inicio': periodo_inicio,
                'periodo_fin': periodo_fin,
                'sede_id': sede.id,
                'estado': 'borrador',
            })

        # Retornar mensaje de éxito
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'name': 'Procesos Importados',
            'res_model': 'importar.procesos.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'message': 'Los procesos de votación han sido importados correctamente.'}
        }
    def descargar_plantilla(self):
            self.ensure_one()
            # Definir el contenido de la plantilla
            output = io.StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
            
            sedes = self.env['uniacme.sede'].search([])  # Obtenemos las sedes
            nombres_sedes = [sede.name for sede in sedes]

            # Escribimos las cabeceras para múltiples procesos de votación
            writer.writerow(['name', 'periodo_inicio', 'periodo_fin', 'sede', 'responsable'])
            writer.writerow(['Nota: Las sedes disponibles son:'] + nombres_sedes)
            writer.writerow(['Ejemplo: Proceso de Ejemplo', '2025-01-01 08:00:00', '2025-01-01 18:00:00', 'nombre sede',])
            writer.writerow(['Ejemplo: Proceso de Ejemplo 2', '2025-02-01 09:00:00', '2025-02-01 17:00:00', 'nombre sede'])
            
            output.seek(0)
            datos_csv = output.getvalue()
            output.close()

            datos_archivo = base64.b64encode(datos_csv.encode('utf-8'))

            attachment = self.env['ir.attachment'].create({
                'name': 'plantilla_procesos_votacion.csv',
                'type': 'binary',
                'datas': datos_archivo,
                'store_fname': 'plantilla_procesos_votacion.csv',
                'mimetype': 'text/csv'
            })

            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/%s?download=true' % attachment.id,
                'target': 'self',
                'name': 'Plantilla Procesos de Votación'
            }
