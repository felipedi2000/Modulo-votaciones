# Módulo de Votaciones UNIACME para Odoo v18

## Descripción
Este módulo permite gestionar el proceso de votaciones de la Universidad UNIACME, incluyendo la creación de sedes, estudiantes, candidatos y votaciones.

## Características
- CRUD para sedes, estudiantes y candidatos.
- Gestión de procesos de votación con estados (Borrador, En proceso, Cerrada).
- Restricción de horarios de votación según la zona horaria de cada sede.
- Página web para que los estudiantes voten.
- Vista pivote en el ERP para ver resultados de votaciones.
- Importación masiva de procesos de votación a través de un wizard.

## Instalación
1. Copiar la carpeta `uniacme_votaciones` en el directorio `addons` de Odoo.
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
