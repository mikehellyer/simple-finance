; Inno Setup script - builds SimpleFinance-Setup.exe from the PyInstaller
; onedir build. Run from the repo root with ISCC.exe (or the "Compile" GUI
; action), after `pyinstaller packaging/pyinstaller/simplefinance.spec` has
; produced dist/SimpleFinance/.
;
;   iscc packaging/windows/installer.iss
;
; AppVersion is overridden from CI with /DAppVersion=X.Y.Z so the installer
; version always matches the GitHub release tag.

#ifndef AppVersion
#define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6C2C8B2E-6E0B-4C7E-9E4E-7A6C1F5D9B21}
AppName=Simple Finance
AppVersion={#AppVersion}
AppPublisher=Mike Hellyer
DefaultDirName={autopf}\SimpleFinance
DefaultGroupName=Simple Finance
UninstallDisplayIcon={app}\SimpleFinance.exe
OutputDir=..\..\dist\installers
OutputBaseFilename=SimpleFinance-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "..\..\dist\SimpleFinance\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Simple Finance"; Filename: "{app}\SimpleFinance.exe"
Name: "{autodesktop}\Simple Finance"; Filename: "{app}\SimpleFinance.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\SimpleFinance.exe"; Description: "Launch Simple Finance"; Flags: nowait postinstall skipifsilent
