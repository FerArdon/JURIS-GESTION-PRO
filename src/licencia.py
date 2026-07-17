import hashlib
import uuid
from datetime import datetime, timedelta

SECRET_KEY = "JURIS_PRO_FER_ARDON_2026"
BASE_DATE = datetime(2024, 1, 1).date()

def get_hardware_id():
    """Genera un ID único corto basado en el hardware del equipo."""
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()[:10].upper()

def verificar_licencia(key):
    """
    Retorna (es_valida, mensaje, dias_restantes)
    """
    try:
        if not key:
            return False, "No hay licencia. Ingrese su clave de producto.", 0
            
        key_raw = key.replace("-", "").strip().upper()
        if len(key_raw) != 20:
            return False, "Formato de clave inválido. Debe tener 20 caracteres.", 0
            
        exp_hex = key_raw[:4]
        signature = key_raw[4:]
        
        hw_id = get_hardware_id()
        
        # Validar firma (Para PC actual)
        expected_sig = hashlib.sha256(f"{exp_hex}{hw_id}{SECRET_KEY}".encode()).hexdigest()[:16].upper()
        
        # Validar firma Universal (Para cualquier PC, en caso de emergencias)
        expected_sig_univ = hashlib.sha256(f"{exp_hex}UNIVERSAL{SECRET_KEY}".encode()).hexdigest()[:16].upper()
        
        if signature != expected_sig and signature != expected_sig_univ:
            return False, "Clave incorrecta o pertenece a otro equipo.", 0
            
        if exp_hex == "FFFF":
            return True, "Licencia Permanente Activada", 9999
            
        # Calcular fecha de expiración
        dias_agregados = int(exp_hex, 16)
        exp_date = BASE_DATE + timedelta(days=dias_agregados)
        today = datetime.now().date()
        
        if today > exp_date:
            return False, "Licencia expirada. Renueve su suscripción.", 0
            
        dias_restantes = (exp_date - today).days
        return True, "Licencia válida.", dias_restantes
        
    except Exception as e:
        return False, "Error de validación de clave.", 0
