"""
ed25519_puro.py — Firma Ed25519 en Python puro (sin dependencias)
==================================================================
VERICUBIC MASTER · SEDCAF

Implementa RFC 8032 (Ed25519) usando solo la biblioteca estándar.
No requiere pip install de nada, por lo que funciona dentro del APK
compilado con Flet en Android, donde las extensiones nativas
(cryptography, pynacl) suelen fallar.

USO EN LA APP (solo verificar):
    from ed25519_puro import verificar
    ok = verificar(firma_bytes, mensaje_bytes, clave_publica_bytes)

USO EN LA PC DEL DESARROLLADOR (firmar):
    from ed25519_puro import firmar, derivar_publica

IMPORTANTE:
    La app NUNCA debe incluir la clave privada. Solo la pública.

Verificado contra los vectores oficiales del RFC 8032 §7.1.
Ejecutar `python ed25519_puro.py` para correr el autotest.
"""

import hashlib

# ---------------------------------------------------------------------------
# Parámetros de la curva edwards25519 (RFC 8032)
# ---------------------------------------------------------------------------
P = 2**255 - 19                                                    # primo del campo
Q = 2**252 + 27742317777372353535851937790883648493                # orden del subgrupo


def _inv(a: int) -> int:
    """Inverso multiplicativo módulo P."""
    return pow(a % P, P - 2, P)


D = (-121665 * _inv(121666)) % P      # constante d de la curva
_I = pow(2, (P - 1) // 4, P)          # raíz cuadrada de -1
_D2 = (2 * D) % P


def _recuperar_x(y: int, signo: int):
    """Recupera la coordenada x a partir de y y el bit de signo."""
    yy = (y * y) % P
    u = (yy - 1) % P
    v = (D * yy + 1) % P
    xx = (u * _inv(v)) % P

    x = pow(xx, (P + 3) // 8, P)
    if (x * x - xx) % P != 0:
        x = (x * _I) % P
    if (x * x - xx) % P != 0:
        return None                   # y no corresponde a ningún punto válido
    if (x & 1) != signo:
        x = (P - x) % P
    return x


# --- Coordenadas extendidas (X:Y:Z:T). Evitan inversiones dentro del bucle,
#     lo que hace la verificación ~100 veces más rápida en un teléfono. ---

def _decodificar_punto(b: bytes):
    """32 bytes comprimidos -> punto extendido, o None si es inválido."""
    if len(b) != 32:
        return None
    n = int.from_bytes(b, "little")
    signo = (n >> 255) & 1
    y = n & ((1 << 255) - 1)
    if y >= P:
        return None
    x = _recuperar_x(y, signo)
    if x is None:
        return None
    return (x, y, 1, (x * y) % P)


def _sumar(A, B):
    """Suma de puntos en coordenadas extendidas."""
    X1, Y1, Z1, T1 = A
    X2, Y2, Z2, T2 = B
    a = ((Y1 - X1) % P) * ((Y2 - X2) % P) % P
    b = ((Y1 + X1) % P) * ((Y2 + X2) % P) % P
    c = T1 * _D2 % P * T2 % P
    d = Z1 * 2 % P * Z2 % P
    e = (b - a) % P
    f = (d - c) % P
    g = (d + c) % P
    h = (b + a) % P
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def _multiplicar(punto, escalar: int):
    """Multiplicación escalar por duplicación y suma."""
    R = (0, 1, 1, 0)                  # elemento neutro
    A = punto
    while escalar > 0:
        if escalar & 1:
            R = _sumar(R, A)
        A = _sumar(A, A)
        escalar >>= 1
    return R


def _iguales(A, B) -> bool:
    """Compara dos puntos proyectivos sin invertir."""
    return (A[0] * B[2] - B[0] * A[2]) % P == 0 and \
           (A[1] * B[2] - B[1] * A[2]) % P == 0


_By = (4 * _inv(5)) % P
_BASE = (_recuperar_x(_By, 0), _By, 1, (_recuperar_x(_By, 0) * _By) % P)


def _a_afin(punto):
    z = _inv(punto[2])
    return (punto[0] * z % P, punto[1] * z % P)


def _codificar_punto(punto) -> bytes:
    x, y = _a_afin(punto)
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def verificar(firma: bytes, mensaje: bytes, clave_publica: bytes) -> bool:
    """
    Verifica una firma Ed25519. Esta es la ÚNICA función que necesita la app.

    Devuelve True solo si la firma fue generada con la clave privada
    correspondiente a `clave_publica` sobre exactamente ese `mensaje`.
    Nunca lanza excepción: ante cualquier dato corrupto devuelve False.
    """
    try:
        if len(firma) != 64 or len(clave_publica) != 32:
            return False
        R = _decodificar_punto(firma[:32])
        if R is None:
            return False
        A = _decodificar_punto(clave_publica)
        if A is None:
            return False
        S = int.from_bytes(firma[32:], "little")
        if S >= Q:                     # rechaza firmas maleables
            return False
        h = int.from_bytes(
            hashlib.sha512(firma[:32] + clave_publica + mensaje).digest(),
            "little",
        ) % Q
        return _iguales(_multiplicar(_BASE, S), _sumar(R, _multiplicar(A, h)))
    except Exception:
        return False


def derivar_publica(clave_privada: bytes) -> bytes:
    """Deriva la clave pública (32 bytes) desde la privada (32 bytes)."""
    if len(clave_privada) != 32:
        raise ValueError("La clave privada debe tener exactamente 32 bytes")
    h = bytearray(hashlib.sha512(clave_privada).digest())
    a = h[:32]
    a[0] &= 248
    a[31] &= 127
    a[31] |= 64
    return _codificar_punto(_multiplicar(_BASE, int.from_bytes(a, "little")))


def firmar(clave_privada: bytes, mensaje: bytes) -> bytes:
    """
    Firma un mensaje. SOLO se usa en la PC del desarrollador.
    Nunca debe llamarse desde la app.
    """
    if len(clave_privada) != 32:
        raise ValueError("La clave privada debe tener exactamente 32 bytes")
    h = bytearray(hashlib.sha512(clave_privada).digest())
    a_bytes = h[:32]
    a_bytes[0] &= 248
    a_bytes[31] &= 127
    a_bytes[31] |= 64
    a = int.from_bytes(a_bytes, "little")
    prefijo = bytes(h[32:])
    A = _codificar_punto(_multiplicar(_BASE, a))

    r = int.from_bytes(hashlib.sha512(prefijo + mensaje).digest(), "little") % Q
    R = _codificar_punto(_multiplicar(_BASE, r))
    k = int.from_bytes(hashlib.sha512(R + A + mensaje).digest(), "little") % Q
    S = (r + k * a) % Q
    return R + S.to_bytes(32, "little")


# ---------------------------------------------------------------------------
# Autotest con los vectores oficiales del RFC 8032 §7.1
# ---------------------------------------------------------------------------

def autotest() -> bool:
    """Valida la implementación contra los vectores oficiales. True si todo pasa."""
    vectores = [
        # (clave_privada, clave_publica_esperada, mensaje, firma_esperada)
        ("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
         "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
         "",
         "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
         "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
        ("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
         "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
         "72",
         "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da"
         "085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
        ("c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7",
         "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025",
         "af82",
         "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac"
         "18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"),
    ]

    fallos = []
    for i, (sk_hex, pk_hex, msg_hex, sig_hex) in enumerate(vectores, 1):
        sk = bytes.fromhex(sk_hex)
        msg = bytes.fromhex(msg_hex)

        pk = derivar_publica(sk)
        if pk.hex() != pk_hex:
            fallos.append(f"vector {i}: clave pública derivada no coincide")

        sig = firmar(sk, msg)
        if sig.hex() != sig_hex:
            fallos.append(f"vector {i}: firma generada no coincide")

        if not verificar(bytes.fromhex(sig_hex), msg, bytes.fromhex(pk_hex)):
            fallos.append(f"vector {i}: no verificó una firma legítima")

        # El mensaje alterado debe ser rechazado
        if verificar(bytes.fromhex(sig_hex), msg + b"\x00", bytes.fromhex(pk_hex)):
            fallos.append(f"vector {i}: aceptó un mensaje alterado")

    if fallos:
        print("AUTOTEST FALLIDO:")
        for f in fallos:
            print("  -", f)
        return False

    print("Autotest OK — 3 vectores del RFC 8032 verificados")
    print("  · Derivación de clave pública correcta")
    print("  · Generación de firma correcta")
    print("  · Verificación de firma correcta")
    print("  · Rechazo de mensajes alterados correcto")
    return True


if __name__ == "__main__":
    import sys
    import time

    ok = autotest()

    inicio = time.time()
    pk = bytes.fromhex("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
    sig = bytes.fromhex(
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    )
    for _ in range(10):
        verificar(sig, b"", pk)
    ms = (time.time() - inicio) * 100
    print(f"\nRendimiento: {ms:.0f} ms por verificación")

    sys.exit(0 if ok else 1)
