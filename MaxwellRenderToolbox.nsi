; NSIS MaxwellRenderToolbox Installer
; Written by Andrew Hazelden
; --------------------------
; 2016-01-31 7.52 pm

SetCompressor /FINAL /SOLID lzma # Slowest and smallest file size
;SetCompressor /FINAL lzma # Medium Speed
;SetCompressor /FINAL ZLIB # Fast for development testing

Unicode true

;--------------------------------
;Include Modern UI
  !include "MUI2.nsh"

;--------------------------------
;Registry value for Add/Remove software

  !define REG_UNINSTALL "Software\Microsoft\Windows\CurrentVersion\Uninstall\MaxwellRenderToolbox" # ${REG_UNINSTALL} 
 
  !define MAXWELLRENDERTOOLBOX_HKLM "Software\Andrew Hazelden\MaxwellRenderToolbox" # ${MAXWELLRENDERTOOLBOX_HKLM}
  
  ;Installer Version Details
  !define VER_DISPLAY "0.1.5.0"
  !define VER_DISPLAY_LONG "0.1.5.0"
  !define VER_MAJOR 0
  !define VER_MINOR 1
  !define VER_REVISION 5
  !define VER_BUILD 0

;--------------------------------
;FileCopy Macro - Check that folder for exists before copying to it
; The /SILENT option will skip showing the Windows file copy dialog

  !define FileCopy `!insertmacro FileCopy`
  !macro FileCopy FilePath TargetDir
    CreateDirectory `${TargetDir}`
    CopyFiles /SILENT `${FilePath}` `${TargetDir}`
  !macroend  
    
;--------------------------------
;General

  ; Refer to MAXWELLRENDERTOOLBOX_DIR as `${MAXWELLRENDERTOOLBOX_DIR}`
  ;!define MAXWELLRENDERTOOLBOX_DIR "C:\Users\Administrator\Documents\GitHub\Maxwell-Render-Toolbox\MaxwellRenderToolbox\"
  ;!define MAXWELLRENDERTOOLBOX_DIR "C:\Users\Andrew\Documents\GitHub\Maxwell-Render-Toolbox\MaxwellRenderToolbox\"
  !define MAXWELLRENDERTOOLBOX_DIR "C:\Users\Russell\Documents\GitHub\Maxwell-Render-Toolbox\MaxwellRenderToolbox\"

  ; Remove the Nullsoft installer branding text
  BrandingText "Maxwell Render Toolbox"

  ;Name and file
  Name "MaxwellRenderToolbox"
  Caption "MaxwellRenderToolbox ${VER_DISPLAY} Setup"
  ;OutFile "C:\Users\Administrator\Desktop\MaxwellRenderToolbox-v${VER_DISPLAY}-windows.exe"
  ;OutFile "C:\Users\Andrew\Desktop\MaxwellRenderToolbox-v${VER_DISPLAY}-windows.exe"
  OutFile "C:\Users\Russell\Desktop\MaxwellRenderToolbox-v${VER_DISPLAY}-windows.exe"
  
  ;Default installation folder
  InstallDir "$PROGRAMFILES64\MaxwellRenderToolbox"

  ;Get installation folder from registry if available
  InstallDirRegKey HKLM "${MAXWELLRENDERTOOLBOX_HKLM}" "Install"

  ;Request Administrator Application privileges for Windows
  RequestExecutionLevel admin
  
;--------------------------------
;Variables

  Var StartMenuFolder
  
;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING
  
;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_INSTFILES
  
  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "${MAXWELLRENDERTOOLBOX_HKLM}" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !define MUI_FINISHPAGE_LINK "Visit the Andrew Hazelden site for Maxwell Render Toolbox news."
  !define MUI_FINISHPAGE_LINK_LOCATION "http://www.andrewhazelden.com/"
  
  !insertmacro MUI_PAGE_FINISH
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

 
;--------------------------------
;Installer Sections

;The MaxwellRenderToolbox section name starts with a dash so it is hidden and is always installed
Section "-MaxwellRenderToolbox" SecMaxwellRenderToolbox

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  ;File /r `C:\Users\Administrator\Documents\GitHub\Maxwell-Render-Toolbox\MaxwellRenderToolbox\*.*`
  File /r `${MAXWELLRENDERTOOLBOX_DIR}\*.*`

  ;Store installation folder
  WriteRegStr HKLM "${MAXWELLRENDERTOOLBOX_HKLM}" "Install" $INSTDIR
  WriteRegDword HKLM "${MAXWELLRENDERTOOLBOX_HKLM}" "VersionMajor" "${VER_MAJOR}"
  WriteRegDword HKLM "${MAXWELLRENDERTOOLBOX_HKLM}" "VersionMinor" "${VER_MINOR}"
  WriteRegDword HKLM "${MAXWELLRENDERTOOLBOX_HKLM}" "VersionRevision" "${VER_REVISION}"
  WriteRegDword HKLM "${MAXWELLRENDERTOOLBOX_HKLM}" "VersionBuild" "${VER_BUILD}"

  ;Setup the MaxwellRenderToolbox Windows Add/Remove Software entry
  ; "${REG_UNINSTALL}"  means "Software\Microsoft\Windows\CurrentVersion\Uninstall\MaxwellRenderToolbox"
  
  WriteRegStr HKLM "${REG_UNINSTALL}" "DisplayName" "Maxwell Render Toolbox"           
  WriteRegStr HKLM "${REG_UNINSTALL}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteRegStr HKLM "${REG_UNINSTALL}" "InstallLocation" "$INSTDIR"
  ;WriteRegStr HKLM "${REG_UNINSTALL}" "DisplayIcon" "$INSTDIR\MaxwellRenderToolbox\icons\maxwell-render-toolbox-icon.ico"  
  WriteRegStr HKLM "${REG_UNINSTALL}" "DisplayVersion" "${VER_DISPLAY}"
  WriteRegDWORD HKLM "${REG_UNINSTALL}" "VersionMajor" "${VER_MAJOR}"
  WriteRegDWORD HKLM "${REG_UNINSTALL}" "VersionMinor" "${VER_MINOR}.${VER_REVISION}"  
  WriteRegStr HKLM "${REG_UNINSTALL}" "Publisher" "Andrew Hazelden"            
  WriteRegStr HKLM "${REG_UNINSTALL}" "Readme" "$INSTDIR\docs\index.html"             
  WriteRegStr HKLM "${REG_UNINSTALL}" "UrlInfoAbout" "http://www.andrewhazelden.com"            
  WriteRegStr HKLM "${REG_UNINSTALL}" "HelpLink" "mailto:andrew@andrewhazelden.com"
  
  WriteRegDWORD HKLM "${REG_UNINSTALL}" "NoModify" "1"
  WriteRegDWORD HKLM "${REG_UNINSTALL}" "NoRepair" "1"
  
  ;Calculate the filesize of the MaxwellRenderToolbox install directory              
  !include "FileFunc.nsh"               
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "${REG_UNINSTALL}" "EstimatedSize" "$0"
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ;Create Start menu shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\MaxwellRenderToolbox Folder.lnk" "$INSTDIR\"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Examples Folder.lnk" "$INSTDIR\examples\"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\MaxwellRenderToolbox Guide.lnk" "$INSTDIR\docs\index.html"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd


;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"
  
;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecMaxwellRenderToolbox ${LANG_ENGLISH} "Install MaxwellRenderToolbox."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMaxwellRenderToolbox} $(DESC_SecMaxwellRenderToolbox)

  !insertmacro MUI_FUNCTION_DESCRIPTION_END


;--------------------------------
; Version Info Field

  VIProductVersion "${VER_DISPLAY_LONG}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "Maxwell Render Toolbox Installer"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "Comments" "Maxwell Render Toolbox - A PyMaxwell Based Pipeline Automation Suite"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "Andrew Hazelden andrew@andrewhazelden.com"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "Copyright © 2015 Andrew Hazelden"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Maxwell Render Toolbox Installer"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${VER_DISPLAY}"

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$INSTDIR\mac_tools.zip"
  
  ;Remove the MaxwellRenderToolbox installed items
  RMDir /r "$INSTDIR\docs"
  RMDir /r "$INSTDIR\examples"
  RMDir /r "$INSTDIR\icons"
  RMDir /r "$INSTDIR\linux_tools"
  RMDir /r "$INSTDIR\scripts"
  RMDir /r "$INSTDIR\sounds"
  RMDir /r "$INSTDIR\tools"
  RMDir /r "$INSTDIR\sourceimages"
  
  ;Remove the MaxwellRenderToolbox install directory
  RMDir "$INSTDIR" 

  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    
  Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\MaxwellRenderToolbox Guide.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\MaxwellRenderToolbox Folder.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Examples Folder.lnk"
  
  RMDir "$SMPROGRAMS\$StartMenuFolder"  
  
  ;Remove the MaxwellRenderToolbox Windows Add/Remove Software entry
  DeleteRegKey HKLM "${REG_UNINSTALL}"
  
  DeleteRegKey /ifempty HKLM "${MAXWELLRENDERTOOLBOX_HKLM}"

SectionEnd  
