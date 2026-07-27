# -*- mode: python ; coding: utf-8 -*-
# Spec file para: Generador de Licencias — JURIS-GESTIÓN-PRO
# Uso privado del proveedor. NO distribuir con el instalador del cliente.

a = Analysis(
    ['generador_licencias.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos pesados que no se usan
        'numpy', 'pandas', 'matplotlib', 'scipy',
        'PIL', 'cv2', 'flask', 'django',
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JGP_Generador_Licencias',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # Sin ventana de consola negra
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # Se puede agregar un .ico si se tiene
    version_file=None,
)
