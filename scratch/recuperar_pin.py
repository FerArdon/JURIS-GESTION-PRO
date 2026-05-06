import sqlite3
import os

db_path = r'e:\1A_A_A_JURIS-GESTIÓN-PRO\data\juris_gestion_pro.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT pin FROM configuracion WHERE id = 1")
    row = cursor.fetchone()
    print(f"PIN actual: {row[0]}")
    conn.close()
else:
    print("Base de datos no encontrada.")
