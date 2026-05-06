import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'juris_gestion_pro.db')

def inyectar_datos_prueba():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Limpiar tablas para evitar duplicados si se corre varias veces
        cursor.execute("DELETE FROM protocolo")
        cursor.execute("DELETE FROM expedientes")
        cursor.execute("DELETE FROM clientes")
        
        # 1. Insertar Clientes
        cursor.execute("INSERT INTO clientes (id_cliente, nombre_completo, rtn, dni, telefono, direccion) VALUES (1, 'Inversiones Verdes S.A.', '0801900323451', '0801-1980-12345', '9988-7766', 'Tegucigalpa')")
        cursor.execute("INSERT INTO clientes (id_cliente, nombre_completo, rtn, dni, telefono, direccion) VALUES (2, 'Marta Alicia Domínguez', '0501199012345', '0501-1990-12345', '9911-2233', 'San Pedro Sula')")
        cursor.execute("INSERT INTO clientes (id_cliente, nombre_completo, rtn, dni, telefono, direccion) VALUES (3, 'Constructora El Pinar', '0801900888888', '0801-1975-88888', '8877-6655', 'Comayagua')")
        
        # 2. Insertar Expedientes
        cursor.execute("INSERT INTO expedientes (id_expediente, id_cliente, juzgado, materia, estado, fecha_creacion) VALUES ('2026-CIV-001', 1, 'Juzgado Letras Civil', 'Civil', 'Activo', '2026-05-01')")
        cursor.execute("INSERT INTO expedientes (id_expediente, id_cliente, juzgado, materia, estado, fecha_creacion) VALUES ('2026-FAM-045', 2, 'Juzgado de Familia', 'Familia', 'En Proceso', '2026-04-15')")
        cursor.execute("INSERT INTO expedientes (id_expediente, id_cliente, juzgado, materia, estado, fecha_creacion) VALUES ('2025-CIV-889', 3, 'Juzgado Letras Civil', 'Civil', 'Cerrado', '2025-10-20')")
        cursor.execute("INSERT INTO expedientes (id_expediente, id_cliente, juzgado, materia, estado, fecha_creacion) VALUES ('2026-LAB-012', 2, 'Juzgado del Trabajo', 'Laboral', 'Activo', '2026-05-04')")
        
        # 3. Insertar Protocolo Notarial
        cursor.execute("INSERT INTO protocolo (numero_instrumento, fecha_otorgamiento, id_cliente, naturaleza_acto, folio_inicio, folio_fin) VALUES (15, '2026-05-01', 1, 'Constitución de Sociedad Mercantil', 45, 52)")
        cursor.execute("INSERT INTO protocolo (numero_instrumento, fecha_otorgamiento, id_cliente, naturaleza_acto, folio_inicio, folio_fin) VALUES (16, '2026-05-03', 2, 'Poder General para Pleitos', 53, 55)")
        cursor.execute("INSERT INTO protocolo (numero_instrumento, fecha_otorgamiento, id_cliente, naturaleza_acto, folio_inicio, folio_fin) VALUES (17, '2026-05-04', 3, 'Contrato de Compraventa de Bien Inmueble', 56, 60)")

        # 4. Insertar Actuaciones (Audiencias)
        cursor.execute("DELETE FROM actuaciones")
        cursor.execute("INSERT INTO actuaciones (id_expediente, tipo_audiencia, fecha_hora, observaciones) VALUES ('2026-CIV-001', '3. Audiencia de Juicio Oral y Público', '2026-05-14 09:00', 'Presentar prueba testifical y peritaje contable')")
        cursor.execute("INSERT INTO actuaciones (id_expediente, tipo_audiencia, fecha_hora, observaciones) VALUES ('2026-FAM-045', '4. Audiencia de Conciliación', '2026-05-20 14:30', 'Llevar propuesta de pensión alimenticia')")

        conn.commit()
        logging.info("✅ Datos de prueba inyectados correctamente en la base de datos local.")
        
    except sqlite3.Error as e:
        logging.error(f"❌ Error al inyectar datos: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    inyectar_datos_prueba()
