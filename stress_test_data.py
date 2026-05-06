import sqlite3
import os
import logging
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'juris_gestion_pro.db')

def generar_datos_estres(num_clientes=5000, num_expedientes=20000, num_audiencias=30000, num_protocolos=2000):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        logging.info("Iniciando inyección masiva de datos para PRUEBA DE ESTRÉS...")
        
        # 0. Limpiar datos previos
        logging.info("Limpiando tablas existentes...")
        cursor.execute("DELETE FROM actuaciones")
        cursor.execute("DELETE FROM protocolo")
        cursor.execute("DELETE FROM expedientes")
        cursor.execute("DELETE FROM clientes")
        
        materias = ['CIV', 'PEN', 'LAB', 'FAM', 'MER', 'ADM', 'AGR', 'CON', 'NOT']
        nombres_base = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Laura", "Jose", "Carmen", "Fernando", "Alicia"]
        apellidos_base = ["Perez", "Gomez", "Lopez", "Rodriguez", "Martinez", "Hernandez", "Garcia", "Fernandez", "Ardon", "Mejia"]
        estados = ['Activo', 'En Proceso', 'Cerrado']
        juzgados = ["Juzgado Letras Civil", "Juzgado de Familia", "Juzgado Penal", "Juzgado Laboral", "Corte Suprema"]
        tipos_audiencia = ["1. Audiencia Inicial", "2. Audiencia Preliminar", "3. Audiencia de Juicio Oral y Público", "4. Audiencia de Conciliación"]
        
        # 1. Insertar Clientes
        logging.info(f"Generando {num_clientes} clientes...")
        clientes_data = []
        for i in range(1, num_clientes + 1):
            nombre = f"{random.choice(nombres_base)} {random.choice(apellidos_base)} {random.choice(apellidos_base)} (Prueba {i})"
            dni = f"{random.randint(100, 999):04d}-{random.randint(1950, 2005)}-{random.randint(0, 99999):05d}"
            tel = f"{random.randint(3000, 9999)}-{random.randint(0, 9999):04d}"
            clientes_data.append((nombre, dni, dni, tel, "Ciudad de Prueba Masiva"))
            
        cursor.executemany("INSERT INTO clientes (nombre_completo, rtn, dni, telefono, direccion) VALUES (?, ?, ?, ?, ?)", clientes_data)
        
        # 2. Insertar Expedientes
        logging.info(f"Generando {num_expedientes} expedientes...")
        expedientes_data = []
        for i in range(1, num_expedientes + 1):
            id_cliente = random.randint(1, num_clientes)
            materia = random.choice(materias)
            id_exp = f"2026-{materia}-{i:05d}"
            juzgado = random.choice(juzgados)
            estado = random.choice(estados)
            expedientes_data.append((id_exp, id_cliente, juzgado, materia, estado))
            
        cursor.executemany("INSERT INTO expedientes (id_expediente, id_cliente, juzgado, materia, estado) VALUES (?, ?, ?, ?, ?)", expedientes_data)
        
        # 3. Insertar Audiencias (Actuaciones)
        logging.info(f"Generando {num_audiencias} audiencias...")
        audiencias_data = []
        start_date = datetime(2026, 1, 1)
        for i in range(1, num_audiencias + 1):
            materia = random.choice(materias)
            id_exp = f"2026-{materia}-{random.randint(1, num_expedientes):05d}"
            tipo = random.choice(tipos_audiencia)
            fecha = start_date + timedelta(days=random.randint(0, 365), hours=random.randint(8, 16))
            monto = round(random.uniform(1000, 500000), 2)
            audiencias_data.append((id_exp, tipo, fecha.strftime("%Y-%m-%d %H:%M"), "Generado por prueba de estrés", monto))
            
        cursor.executemany("INSERT INTO actuaciones (id_expediente, tipo_audiencia, fecha_hora, observaciones, monto_involucrado) VALUES (?, ?, ?, ?, ?)", audiencias_data)

        conn.commit()
        logging.info("✅ PRUEBA DE ESTRÉS COMPLETADA: Datos inyectados correctamente.")
        
    except sqlite3.Error as e:
        logging.error(f"❌ Error crítico al inyectar datos de estrés: {e}")
        conn.rollback()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    generar_datos_estres()