import os
from datetime import datetime, timedelta

from src.ed25519_puro import firmar
from src.licencia import BASE_DATE, PERMANENTE, mensaje_licencia, mensaje_reset, formatear_base32

# Clave PRIVADA Ed25519: vive FUERA del repositorio.
#   %USERPROFILE%\\.sedcaf_keys\\jurisgestion.key  (o la variable JURIS_PRIVATE_KEY_FILE)
# Respáldela en un gestor de contraseñas: sin ella no se pueden emitir licencias.
def _clave_privada():
    ruta = os.environ.get("JURIS_PRIVATE_KEY_FILE") or os.path.join(
        os.path.expanduser("~"), ".sedcaf_keys", "jurisgestion.key")
    with open(ruta, "r", encoding="ascii") as f:
        return bytes.fromhex(f.read().strip())


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

    exp_dias = (exp_date - BASE_DATE).days if exp_date else PERMANENTE
    firma = firmar(_clave_privada(), mensaje_licencia(hw_id, exp_dias))
    return formatear_base32(exp_dias.to_bytes(2, "big") + firma)


def generar_codigo_reset(hw_id):
    """Código para restablecer el PIN de un cliente: sirve solo para ese equipo y hoy (±1 día)."""
    firma = firmar(_clave_privada(), mensaje_reset(hw_id, datetime.now().date()))
    return formatear_base32(firma)


if __name__ == '__main__':
    print("=================================================")
    print("   GENERADOR DE CLAVES JURIS-GESTIÓN-PRO         ")
    print("=================================================")
    print("  1 - Licencia        2 - Código de reset de PIN")
    modo = input("\nOpción (1/2): ").strip()
    hw = input("Hardware ID del cliente (Ej. 8A3F9D2B41; vacío = UNIVERSAL): ").strip().upper()
    if not hw:
        hw = "UNIVERSAL"
        print(" -> Se usará clave UNIVERSAL (sirve en cualquier equipo; úsela con cuidado).")

    if modo == "2":
        lic = generar_codigo_reset(hw)
    else:
        print("\nTipos de Licencia:")
        print("  10D  - Prueba de 10 días")
        print("  1M   - Suscripción de 1 mes")
        print("  6M   - Suscripción de 6 meses")
        print("  1Y   - Suscripción de 1 año")
        print("  PERM - Pago único de por vida")
        tipo = input("\nTipo (10D, 1M, 6M, 1Y, PERM): ").strip().upper()
        lic = generar_licencia(hw, tipo)

    print("\n-------------------------------------------------")
    if "ERROR" in lic:
        print(lic)
    else:
        print("✅ CLAVE GENERADA CON ÉXITO:")
        print(f"\n   {lic}\n")
    print("-------------------------------------------------")
    print("Envíe la clave completa al cliente (cópiela y péguela).")
    input("Presione Enter para salir...")
