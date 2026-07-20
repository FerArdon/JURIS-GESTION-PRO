# -*- mode: python ; coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════╗
# ║  JURIS-GESTIÓN-PRO — Spec de compilación PyInstaller        ║
# ║  Fer Ardón · 2026                                           ║
# ╚══════════════════════════════════════════════════════════════╝

import sys
from pathlib import Path
import webview
import os

ROOT = Path(SPECPATH)  # directorio raíz del proyecto

# ── Archivos de datos que deben ir dentro del .exe ─────────────
_webview_lib = os.path.join(os.path.dirname(webview.__file__), 'lib')

added_files = [
    # UI principal (HTML + todo el frontend)
    (str(ROOT / 'ui' / 'juris_gestion_pro_app.html'), 'ui'),
    # Activos gráficos
    (str(ROOT / 'assets' / 'custom_logo.ico'),  'assets'),
    (str(ROOT / 'assets' / 'custom_logo.png'),         'assets'),
    (str(ROOT / 'assets' / 'juris_gestion_pro_logo.png'), 'assets'),
    # Plantillas de escritos legales (toda la carpeta con subcarpetas)
    (str(ROOT / 'plantillas'), 'plantillas'),
    # Config por defecto (se copia al primer arranque)
    (str(ROOT / 'config' / 'incidentes_procesales.json'), 'config'),
    # Módulos src
    (str(ROOT / 'src' / 'database.py'),  'src'),
    (str(ROOT / 'src' / 'licencia.py'),  'src'),
    (str(ROOT / 'src' / 'seguridad.py'), 'src'),
    # WebView2 interop DLLs (requeridos por pywebview en modo frozen)
    (_webview_lib, 'webview/lib'),
]

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        # pywebview
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.cef',
        # clr (pythonnet) — el módulo Python se llama 'clr', no 'System.*'
        'clr',
        # sqlite3 (stdlib)
        'sqlite3',
        '_sqlite3',
        # plyer (notificaciones nativas de Windows) — carga backends por plugin,
        # PyInstaller no los detecta automaticamente
        'plyer.platforms.win.notification',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy', 'pandas', 'matplotlib', 'scipy',
        'PIL', 'cv2', 'flask', 'django',
        'IPython', 'notebook',
    ],
    noarchive=False,
    optimize=1,   # optimize=2 puede romper algunas libs .NET
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JURIS_GESTION_PRO',
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
    icon=str(ROOT / 'assets' / 'custom_logo.ico'),
    version_file=None,
)
