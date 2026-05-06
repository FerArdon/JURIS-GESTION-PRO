
import sqlite3
import os
import sys

# Añadir el path para importar database y main si es necesario
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_stress_test():
    db_path = "juris_gestion.db"
    print(f"--- INICIANDO PRUEBA DE ESTRÉS NOTARIAL ---")
    print(f"Base de datos: {db_path}")

    if not os.path.exists(db_path):
        print("ERROR: Base de datos no encontrada. Ejecute la aplicación primero.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # 1. Limpiar tabla protocolo para la prueba (opcional, pero mejor para control)
        # No borraremos, solo insertaremos hasta fallar.
        
        # 2. Obtener configuración
        cursor.execute("SELECT tomo_actual, limite_tomo, exequatur FROM configuracion WHERE id = 1")
        config = cursor.fetchone()
        tomo = config['tomo_actual']
        limite = config['limite_tomo']
        print(f"Configuración detectada: Tomo {tomo}, Límite {limite} folios.")

        # 3. Insertar instrumentos de 40 folios cada uno (5 instrumentos = 200 folios)
        # El 6to debería fallar.
        
        # Primero, ver cuántos folios hay ya
        cursor.execute("SELECT SUM(folio_fin - folio_inicio + 1) as total FROM protocolo WHERE numero_tomo = ?", (tomo,))
        res = cursor.fetchone()
        folios_actuales = res['total'] or 0
        print(f"Folios actuales en el Tomo {tomo}: {folios_actuales}")

        folios_restantes = limite - folios_actuales
        print(f"Espacio disponible: {folios_restantes} folios.")

        # Necesitamos un cliente para las pruebas
        cursor.execute("SELECT id_cliente FROM clientes LIMIT 1")
        cliente = cursor.fetchone()
        if not cliente:
            print("Creando cliente de prueba...")
            cursor.execute("INSERT INTO clientes (nombre_completo, dni) VALUES (?, ?)", ("Cliente de Prueba", "0000-0000-00000"))
            conn.commit()
            cursor.execute("SELECT id_cliente FROM clientes LIMIT 1")
            cliente = cursor.fetchone()

        id_cliente = cliente['id_cliente']

        # Intentar llenar el tomo
        instrumentos_creados = 0
        while folios_actuales < limite:
            # Intentamos insertar uno de 10 folios
            folios_a_insertar = 10
            # Simular la lógica de main.py
            cursor.execute("SELECT MAX(numero_instrumento) as max_num, MAX(folio_fin) as max_folio FROM protocolo")
            last = cursor.fetchone()
            next_num = (last['max_num'] + 1) if last['max_num'] else 1
            next_folio_start = (last['max_folio'] + 1) if last['max_folio'] else 1
            next_folio_end = next_folio_start + folios_a_insertar - 1

            if next_folio_end > limite:
                print(f"\n>>> INTENTO DE DESBORDAMIENTO DETECTADO <<<")
                print(f"Instrumento {next_num} requiere folios {next_folio_start}-{next_folio_end}.")
                print(f"Límite legal: {limite}. ESTADO: BLOQUEO CORRECTO (Simulado).")
                break
            
            cursor.execute('''
                INSERT INTO protocolo (numero_instrumento, fecha_otorgamiento, id_cliente, naturaleza_acto, folio_inicio, folio_fin, numero_tomo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (next_num, '2026-05-06', id_cliente, "Acto de Prueba Stress", next_folio_start, next_folio_end, tomo))
            
            folios_actuales = next_folio_end
            instrumentos_creados += 1
            print(f"Insertado Instrumento {next_num}: Folios {next_folio_start}-{next_folio_end} (Total: {folios_actuales})")

        conn.commit()
        print(f"\n--- PRUEBA FINALIZADA ---")
        print(f"Instrumentos creados en esta sesión: {instrumentos_creados}")
        print(f"Estado final del Tomo {tomo}: {folios_actuales}/{limite} folios.")

    except Exception as e:
        print(f"ERROR DURANTE LA PRUEBA: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_stress_test()
