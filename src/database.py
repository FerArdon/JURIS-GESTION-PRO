import sqlite3
import os
import logging

# Configuración de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rutas relativas para garantizar que la app funcione sin importar donde se instale
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'juris_gestion_pro.db')

def inicializar_db():
    """Crea la estructura de la base de datos (Fase 1 de los Cimientos)"""
    
    # Asegurar que el directorio 'data' exista
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Tabla de Configuración Institucional (Marca Blanca y Auditoría)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                nombre_despacho TEXT NOT NULL,
                lema_legal TEXT,
                ruta_logo TEXT,
                pie_pagina_info TEXT,
                api_key_ai TEXT,
                exequatur TEXT DEFAULT 'PENDIENTE',
                tomo_actual INTEGER DEFAULT 1,
                folio_inicial_tomo INTEGER DEFAULT 1,
                limite_tomo INTEGER DEFAULT 200
            )
        ''')
        
        # Migración segura: añadir columnas si la tabla ya existía sin ellas
        # (Debe ejecutarse antes del INSERT para evitar errores si la BD es de una versión anterior)
        migraciones_config = [
            "ALTER TABLE configuracion ADD COLUMN exequatur TEXT DEFAULT '0000-0000'",
            "ALTER TABLE configuracion ADD COLUMN tomo_actual INTEGER DEFAULT 1",
            "ALTER TABLE configuracion ADD COLUMN folio_inicial_tomo INTEGER DEFAULT 1",
            "ALTER TABLE configuracion ADD COLUMN limite_tomo INTEGER DEFAULT 200"
        ]
        for sql in migraciones_config:
            try:
                cursor.execute(sql)
            except sqlite3.OperationalError:
                pass

        # Insertar configuración por defecto si no existe
        cursor.execute('''
            INSERT OR IGNORE INTO configuracion (
                id, nombre_despacho, lema_legal, ruta_logo, exequatur, tomo_actual, folio_inicial_tomo, limite_tomo
            )
            VALUES (1, 'Mi Despacho Legal', 'Justicia y Transparencia', 'assets/juris_gestion_pro_logo.png', '0000-0000', 1, 1, 200)
        ''')

        # 2. Tabla de Clientes (Módulo CRM)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_completo TEXT NOT NULL,
                rtn TEXT UNIQUE,
                dni TEXT UNIQUE NOT NULL,
                telefono TEXT,
                correo TEXT,
                direccion TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE
            )
        ''')

        # 3. Tabla de Expedientes (Control de Casos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expedientes (
                id_expediente TEXT PRIMARY KEY,
                id_cliente INTEGER NOT NULL,
                juzgado TEXT,
                materia TEXT,
                estado TEXT CHECK(estado IN ('Activo', 'En Proceso', 'Cerrado')) DEFAULT 'Activo',
                tipo_resolucion TEXT,
                fecha_creacion DATE DEFAULT CURRENT_DATE,
                fecha_cierre DATE,
                FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
            )
        ''')

        # 4. Tabla de Actuaciones (Observaciones, Audiencias y Fechas Clave)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actuaciones (
                id_actuacion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_expediente TEXT NOT NULL,
                tipo_audiencia TEXT,
                fecha_hora DATETIME,
                observaciones TEXT,
                incidentes TEXT,
                monto_involucrado REAL DEFAULT 0.0,
                FOREIGN KEY (id_expediente) REFERENCES expedientes (id_expediente)
            )
        ''')

        # 5. Tabla del Libro de Protocolo Notarial (Con soporte de Tomo)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protocolo (
                id_instrumento INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_instrumento INTEGER UNIQUE NOT NULL,
                fecha_otorgamiento DATE NOT NULL,
                id_cliente INTEGER NOT NULL,
                naturaleza_acto TEXT NOT NULL,
                folio_inicio INTEGER NOT NULL,
                folio_fin INTEGER NOT NULL,
                numero_tomo INTEGER DEFAULT 1,
                FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
            )
        ''')

        conn.commit()
        
        # Migración segura para otras tablas (protocolo)
        try:
            cursor.execute("ALTER TABLE protocolo ADD COLUMN numero_tomo INTEGER DEFAULT 1")
            conn.commit()
        except sqlite3.OperationalError:
            pass # Las columnas ya existen

        logging.info(f"Base de datos inicializada correctamente en: {DB_PATH}")
        
    except sqlite3.Error as e:
        logging.error(f"Error al inicializar la base de datos: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    logging.info("Iniciando Fase 1: Creación de Cimientos de Datos...")
    inicializar_db()
