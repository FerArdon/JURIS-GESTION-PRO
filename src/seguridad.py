import os
import zipfile
from datetime import datetime
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

def ejecutar_escudo_datos():
    """Ejecuta el backup automático (Escudo de Datos) comprimiendo la BD y configuraciones."""
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Extensión personalizada para mayor profesionalismo
        backup_filename = f"escudo_jgp_{timestamp}.jgpbackup"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Elementos críticos a respaldar
        carpetas = ['data', 'config', 'plantillas']
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for carpeta in carpetas:
                ruta_carpeta = os.path.join(BASE_DIR, carpeta)
                if os.path.exists(ruta_carpeta):
                    for root, dirs, files in os.walk(ruta_carpeta):
                        for file in files:
                            # Ignorar archivos temporales de SQLite
                            if not file.endswith('-journal'):
                                filepath = os.path.join(root, file)
                                arcname = os.path.relpath(filepath, BASE_DIR)
                                zipf.write(filepath, arcname)
                                
        logging.info(f"ESCUDO DE DATOS ACTIVO: Respaldo de seguridad creado exitosamente ({backup_filename}).")
        return True
    except Exception as e:
        logging.error(f"Error crítico en el Escudo de Datos: {e}")
        return False
