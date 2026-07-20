; ╔══════════════════════════════════════════════════════════════╗
; ║  JURIS-GESTIÓN-PRO — Script de Instalación Inno Setup (32-Bit)║
; ║  Autor: Fer Ardón · 2026                                    ║
; ║  Genera: JGP_Setup_v1.0_x86.exe                             ║
; ╚══════════════════════════════════════════════════════════════╝
;
; INSTRUCCIONES:
;   1. Asegúrate de que dist\JURIS_GESTION_PRO.exe ya existe
;      (compilado con PyInstaller 32-bit usando la spec correspondiente).
;   2. Abre este archivo en Inno Setup Compiler.
;   3. Presiona Ctrl+F9 para compilar → genera Output\JGP_Setup_v1.0_x86.exe

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
; Se instala en Program Files (x86) en sistemas de 64-bit, o Program Files en 32-bit
DefaultDirName={autopf}\{#MyAppName}

DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Carpeta de salida del instalador generado
OutputDir=Output
OutputBaseFilename=JGP_Setup_v{#MyAppVersion}_x86

; ── Apariencia del instalador ──────────────────────────────────
SetupIconFile={#MyAppIcon}

; ── Compresión ────────────────────────────────────────────────
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
InternalCompressLevel=ultra64

; ── Compatibilidad y permisos ─────────────────────────────────
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
; Nota: Al no definir ArchitecturesAllowed, funciona en arquitecturas de 32-bit y 64-bit

; ── Modo de instalación ───────────────────────────────────────
DisableDirPage=no
DisableReadyPage=no
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName} (32-Bit)

; ── Reinicio ──────────────────────────────────────────────────
RestartIfNeededByRun=no
CloseApplications=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Iconos adicionales:"; Flags: unchecked

[Files]
; ── Ejecutable principal (compilado por PyInstaller 32-bit) ────
Source: "{#DistDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Acceso directo en el menú de inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
; Desinstalar en el menú
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\{#MyAppExeName}"
; Acceso directo en escritorio (solo si el usuario lo eligió)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssDone then
  begin
    // Instalación completada exitosamente
  end;
end;
