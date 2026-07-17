import hashlib
from datetime import datetime, timedelta

SECRET_KEY = "JURIS_PRO_FER_ARDON_2026"
BASE_DATE = datetime(2024, 1, 1).date()

def generar_licencia(hw_id, tipo):
    today = datetime.now().date()
    
    if tipo == '10D':
        exp_date = today + timedelta(days=10)
    elif tipo == '1M':
        exp_date = today + timedelta(days=30)
    elif tipo == '6M':
        exp_date = today + timedelta(days=180)
    elif tipo == '1Y':
        exp_date = today + timedelta(days=365)
    elif tipo == 'PERMANENTE' or tipo == 'PERM':
        exp_date = None
    else:
        return "ERROR: Tipo inválido."
        
    if exp_date:
        dias_totales = (exp_date - BASE_DATE).days
        exp_hex = f"{dias_totales:04X}"
    else:
        exp_hex = "FFFF"
        
    hw_id = hw_id.strip().upper()
    signature = hashlib.sha256(f"{exp_hex}{hw_id}{SECRET_KEY}".encode()).hexdigest()[:16].upper()
    
    raw_key = exp_hex + signature
    # Formatear como XXXXX-XXXXX-XXXXX-XXXXX
    formatted_key = f"{raw_key[:5]}-{raw_key[5:10]}-{raw_key[10:15]}-{raw_key[15:20]}"
    return formatted_key

if __name__ == '__main__':
    print("=================================================")
    print("   GENERADOR DE CLAVES JURIS-GESTIÓN-PRO         ")
    print("=================================================")
    hw = input("1. Ingrese el Hardware ID del cliente (Ej. 8A3F9D2B41): ").strip().upper()
    if not hw:
        hw = "UNIVERSAL"
        print(" -> Se usará clave UNIVERSAL.")
        
    print("\nTipos de Licencia:")
    print("  10D  - Prueba de 10 días")
    print("  1M   - Suscripción de 1 mes")
    print("  6M   - Suscripción de 6 meses")
    print("  1Y   - Suscripción de 1 año")
    print("  PERM - Pago único de por vida")
    tipo = input("\n2. Ingrese tipo (10D, 1M, 6M, 1Y, PERM): ").strip().upper()

    lic = generar_licencia(hw, tipo)
    print("\n-------------------------------------------------")
    if "ERROR" in lic:
        print(lic)
    else:
        print("✅ CLAVE GENERADA CON ÉXITO:")
        print(f"\n   {lic}\n")
    print("-------------------------------------------------")
    print("Envíe esta clave de 20 caracteres al cliente.")
    input("Presione Enter para salir...")
