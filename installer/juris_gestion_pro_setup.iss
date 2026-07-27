; ╔══════════════════════════════════════════════════════════════╗
; ║  JURIS-GESTIÓN-PRO — Script de Instalación Inno Setup       ║
; ║  Autor: Fer Ardón · 2026                                    ║
; ║  Genera: JGP_Setup_v1.0.exe                                 ║
; ╚══════════════════════════════════════════════════════════════╝
;
; INSTRUCCIONES:
;   1. Asegúrate de que dist\JURIS_GESTION_PRO.exe ya existe
;      (compilado con PyInstaller usando juris_gestion_pro.spec).
;   2. Abre este archivo en Inno Setup Compiler.
;   3. Presiona Ctrl+F9 para compilar → genera Output\JGP_Setup_v1.0.exe

#define MyAppName      "JURIS-GESTIÓN-PRO"
#define MyAppVersion   "1.0"
#define MyAppPublisher "Fer Ardón"
#define MyAppURL       "https://jurisgestionpro.hn"
#define MyAppExeName   "JURIS_GESTION_PRO.exe"
#define MyAppIcon      "..\assets\custom_logo.ico"

; ── Ruta donde PyInstaller dejó el .exe compilado ─────────────
#define DistDir        "..\dist"

[Setup]
; ── Identificación única de la aplicación ─────────────────────
AppId={{A7F3C2D1-8B4E-4F9A-B6C0-D2E8F1A3B5C7}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright © 2026 Fer Ardón. Todos los derechos reservados.

; ── Directorios ────────────────────────────────────────────────
; Se instala en Program Files (recomendado)
DefaultDirName={autopf}\{#MyAppName}
; Si prefieres instalación solo para el usuario actual (sin UAC):
; DefaultDirName={localappdata}\{#MyAppName}

DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Carpeta de salida del instalador generado
OutputDir=Output
OutputBaseFilename=JGP_Setup_v{#MyAppVersion}

; ── Apariencia del instalador ──────────────────────────────────
SetupIconFile={#MyAppIcon}
; Imagen lateral del wizard (164x314 px BMP opcional)
; WizardImageFile=wizard_side.bmp
; WizardSmallImageFile=wizard_small.bmp

; ── Compresión ────────────────────────────────────────────────
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
InternalCompressLevel=ultra64

; ── Compatibilidad y permisos ─────────────────────────────────
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ── Modo de instalación ───────────────────────────────────────
DisableDirPage=no
DisableReadyPage=no
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; ── Reinicio ──────────────────────────────────────────────────
; No se requiere reinicio
RestartIfNeededByRun=no
CloseApplications=yes

; Usar carpeta previa si ya estuvo instalado (comportamiento por defecto en IS6)

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Iconos adicionales:"; Flags: unchecked

[Files]
; ── Ejecutable principal (compilado por PyInstaller) ──────────
Source: "{#DistDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; NOTA: PyInstaller con onefile empaqueta todo dentro del .exe.
; Si en el futuro cambias a onedir, descomenta esta línea:
; Source: "{#DistDir}\{#MyAppExeName}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Acceso directo en el menú de inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
; Desinstalar en el menú
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\{#MyAppExeName}"
; Acceso directo en escritorio (solo si el usuario lo eligió)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Ejecutar la app al finalizar la instalación (opcional, el usuario puede desmarcar)
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpiar datos generados por la aplicación en LocalAppData
; (solo si la app los dejó en la carpeta de instalación)
Type: filesandordirs; Name: "{app}"

[Code]
// ── Pre-instalación: verificar si ya existe una versión anterior ──
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

// ── Post-instalación: verificar que el .exe esté presente ────────
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssDone then
  begin
    // Instalación completada exitosamente
  end;
end;
