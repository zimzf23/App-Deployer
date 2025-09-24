@echo off
setlocal ENABLEDELAYEDEXPANSION

:: Try to locate nssm.exe
set "NSSM_EXE="
for /f "usebackq delims=" %%I in (`where nssm 2^>nul`) do set "NSSM_EXE=%%I"

:: Fallback common locations
if not defined NSSM_EXE if exist "C:\nssm\nssm.exe" set "NSSM_EXE=C:\nssm\nssm.exe"
if not defined NSSM_EXE if exist "%LOCALAPPDATA%\nssm\nssm.exe" set "NSSM_EXE=%LOCALAPPDATA%\nssm\nssm.exe"

if defined NSSM_EXE (
  for %%D in ("%NSSM_EXE%") do set "NSSM_DIR=%%~dpD"
  set "NSSM_DIR=!NSSM_DIR:~0,-1!"
  echo [+] Found: "!NSSM_EXE!"
) else (
  echo [i] nssm.exe not found; will still scrub PATH entries.
  set "NSSM_DIR=C:\nssm"
)

:: Delete NSSM folder if present
if exist "!NSSM_DIR!\nssm.exe" (
  echo [+] Removing "!NSSM_DIR!" ...
  rmdir /S /Q "!NSSM_DIR!" 2>nul
  if exist "!NSSM_DIR!" echo [!] Could not remove "!NSSM_DIR!" (in use? Admin?).
) else (
  echo [i] NSSM folder not present at "!NSSM_DIR!".
)

:: ---- Clean USER PATH ----
for /f "tokens=2,*" %%A in ('reg query HKCU\Environment /v Path 2^>nul ^| find /I "Path"') do set "USERPATH=%%B"
if defined USERPATH (
  set "NEW_U_PATH=!USERPATH:;!NSSM_DIR!;=;!"
  set "NEW_U_PATH=!NEW_U_PATH:!NSSM_DIR!;=!"
  set "NEW_U_PATH=!NEW_U_PATH:;!NSSM_DIR!=;!"
  if /I "!NEW_U_PATH!" NEQ "!USERPATH!" (
    setx Path "!NEW_U_PATH!" >nul
    echo [+] Cleaned USER PATH.
  ) else (
    echo [i] USER PATH had no NSSM entry.
  )
)

:: ---- Clean SYSTEM PATH (if admin) ----
set "IS_ADMIN=0"
net session >nul 2>&1 && set "IS_ADMIN=1"
if "%IS_ADMIN%"=="1" (
  for /f "tokens=2,*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul ^| find /I "Path"') do set "SYSPATH=%%B"
  if defined SYSPATH (
    set "NEW_S_PATH=!SYSPATH:;!NSSM_DIR!;=;!"
    set "NEW_S_PATH=!NEW_S_PATH:!NSSM_DIR!;=!"
    set "NEW_S_PATH=!NEW_S_PATH:;!NSSM_DIR!=;!"
    if /I "!NEW_S_PATH!" NEQ "!SYSPATH!" (
      setx /M Path "!NEW_S_PATH!" >nul
      echo [+] Cleaned SYSTEM PATH.
    ) else (
      echo [i] SYSTEM PATH had no NSSM entry.
    )
  )
) else (
  echo [i] Not admin: skipping SYSTEM PATH cleanup.
)

echo ✅ NSSM uninstalled (or not present). Open a NEW terminal to refresh PATH.
endlocal
exit /b 0
