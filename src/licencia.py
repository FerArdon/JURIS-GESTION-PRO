"""
Licencias de Juris Gestión Pro — firma Ed25519.

La app lleva SOLO la clave pública: sirve para comprobar licencias, pero no para
crearlas. La clave privada vive únicamente en la PC del emisor (fuera del repositorio).

Formato de la clave: base32 en grupos de 5 (106 caracteres), que contiene
    vencimiento (2 bytes, días desde BASE_DATE; 0xFFFF = permanente) + firma Ed25519 (64 bytes)
La firma cubre: dominio | ID de equipo (o UNIVERSAL) | vencimiento.
"""
import base64
import hashlib
import uuid
from datetime import datetime, timedelta

from .ed25519_puro import verificar

PUBLIC_KEY = bytes.fromhex("bcd3fd132998f343e5af8d6579ee1a8aaca33ef6f5f4a91ec46ad8a247e819a0")
DOMINIO_LICENCIA = b"JURIS-LIC-v2|"
DOMINIO_RESET = b"JURIS-RESETPIN-v2|"
BASE_DATE = datetime(2024, 1, 1).date()
PERMANENTE = 0xFFFF


def get_hardware_id():
    """Genera un ID único corto basado en el hardware del equipo."""
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()[:10].upper()


def mensaje_licencia(hw_id, exp_dias):
    """Mensaje que firma el emisor (también lo usa el generador)."""
    return DOMINIO_LICENCIA + hw_id.strip().upper().encode("utf-8") + b"|" + exp_dias.to_bytes(2, "big")


def mensaje_reset(hw_id, fecha):
    """Mensaje del código de restablecimiento de PIN: válido para un equipo y un día."""
    return DOMINIO_RESET + hw_id.strip().upper().encode("utf-8") + b"|" + fecha.strftime("%Y%m%d").encode()


def formatear_base32(datos):
    b32 = base64.b32encode(datos).decode("ascii").rstrip("=")
    return "-".join(b32[i:i + 5] for i in range(0, len(b32), 5))


def _decodificar_base32(texto):
    limpio = texto.replace("-", "").replace(" ", "").strip().upper()
    if not limpio:
        return None
    try:
        return base64.b32decode(limpio + "=" * (-len(limpio) % 8))
    except Exception:
        return None


def verificar_licencia(key):
    """
    Retorna (es_valida, mensaje, dias_restantes)
    """
    try:
        if not key:
            return False, "No hay licencia. Ingrese su clave de producto.", 0

        crudo = _decodificar_base32(key)
        if crudo is None or len(crudo) != 66:
            return False, "Formato de clave inválido. Pegue la clave completa recibida.", 0

        exp_dias = int.from_bytes(crudo[:2], "big")
        firma = crudo[2:]

        # Firma válida para este equipo, o clave UNIVERSAL (cualquier equipo) emitida por SEDCAF.
        hw_id = get_hardware_id()
        if not (verificar(firma, mensaje_licencia(hw_id, exp_dias), PUBLIC_KEY)
                or verificar(firma, mensaje_licencia("UNIVERSAL", exp_dias), PUBLIC_KEY)):
            return False, "Clave incorrecta o pertenece a otro equipo.", 0

        if exp_dias == PERMANENTE:
            return True, "Licencia Permanente Activada", 9999

        exp_date = BASE_DATE + timedelta(days=exp_dias)
        today = datetime.now().date()
        if today > exp_date:
            return False, "Licencia expirada. Renueve su suscripción.", 0

        return True, "Licencia válida.", (exp_date - today).days

    except Exception:
        return False, "Error de validación de clave.", 0


def verificar_codigo_reset(codigo):
    """True si el código de restablecimiento fue firmado por SEDCAF para este equipo hoy (±1 día)."""
    try:
        firma = _decodificar_base32(codigo)
        if firma is None or len(firma) != 64:
            return False
        hw_id = get_hardware_id()
        hoy = datetime.now().date()
        return any(
            verificar(firma, mensaje_reset(hw_id, hoy + timedelta(days=d)), PUBLIC_KEY)
            for d in (-1, 0, 1)
        )
    except Exception:
        return False
