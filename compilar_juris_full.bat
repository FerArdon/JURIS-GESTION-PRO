@echo off
chcp 65001 >nul
echo ============================================================
echo   JURIS-GESTION PRO — Compilacion y Empaquetado
echo   Fer Ardon · SEDCAF · 2026
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] Limpiando builds anteriores...
if exist dist\JURIS_GESTION_PRO.exe del /f /q dist\JURIS_GESTION_PRO.exe
if exist build rmdir /s /q build

echo [2/3] Compilando EXE con PyInstaller...
pyinstaller --clean juris_gestion_pro.spec
if errorlevel 1 (
    echo.
    echo ERROR: Fallo la compilacion. Revisa los logs arriba.
    pause
    exit /b 1
)

echo.
echo [3/3] EXE generado correctamente:
echo        dist\JURIS_GESTION_PRO.exe
echo.

set /p run_inno="Compilar instalador con Inno Setup? (s/n): "
if /i "%run_inno%"=="s" (
    echo Ejecutando Inno Setup...
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\juris_gestion_pro_setup.iss
    if errorlevel 1 (
        echo ERROR: Fallo Inno Setup.
    ) else (
        echo Instalador creado en installer\Output\
    )
)

echo.
echo ============================================================
echo   Compilacion completada exitosamente!
echo ============================================================
pause
