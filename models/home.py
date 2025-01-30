from odoo import models, fields

class Home(models.Model):
    _name = 'home'
    _description = 'Vista de Bienvenida'

    name = fields.Char(string="Nombre", default="¡Bienvenido al Módulo!")
    description = fields.Text(string="Descripción", default="Seleccione una opción en el menú para continuar.")
