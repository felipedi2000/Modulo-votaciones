{
    'name': 'Votaciones UNIACME',
    'version': '1.0',
    'category': 'Tools',
    'author': 'felipe',
    'website': '',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/home_view.xml',
        'data/data.xml',
        'views/edtudiantes_view.xml',
        'views/procesos_view.xml',
        'views/votos_wizard_view.xml',
        'views/import_view.xml',
        'views/sedes_views.xml',
        'views/pivot_votos_view.xml',
        'views/menu.xml'
    ],
    'description': """
        Módulo para gestionar los procesos de votaciones en la universidad UNIACME.
        Permite crear y gestionar procesos de votación en distintas sedes,
        agregar candidatos, realizar votaciones, y consultar resultados.
        
        Funciones principales:
        - Crear y gestionar sedes, estudiantes, candidatos y procesos de votación.
        - Los estudiantes pueden votar solo una vez por proceso.
        - Validación de votación según la zona horaria de cada sede.
        - Importación de procesos de votación mediante archivo CSV.
        - Generación de informes de resultados por candidato.
    """,
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['pytz'],
    },
        'assets': {
        'web.assets_backend': [
            'votaciones_uniacme/static/src/scss/*',
        ],
    },
}