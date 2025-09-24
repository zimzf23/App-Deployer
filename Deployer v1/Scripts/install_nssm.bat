@echo off
setlocal ENABLEDELAYEDEXPANSION

:: ================
:: CONFIG
:: ================
set "NSSM_URL=https://nssm.cc/release/nssm-2.24.zip"
set "PREFERRED_DIR=C:\nssm"

:: Decide install dir (try C:\nssm, fallback to user profile if not admin)
set "NSSM_DIR=%PREFERRED_DIR%"
mkdir "%NSSM_DIR%" >nul 2>&1
if errorlevel 1 (
  set "NSSM_DIR=%LOCALAPPDATA%\nssm"
  mkdir "%NSSM_DIR%" >nul 2>&1
)

set "NSSM_ZIP=%NSSM_DIR%\nssm.zip"
set "NSSM_EXE=%NSSM_DIR%\nssm.exe"

echo [+] NSSM target directory: "%NSSM_DIR%"

:: Skip if already installed
if exist "%NSSM_EXE%" (
  echo [i] nssm.exe already present at "%NSSM_EXE%".
  goto add_to_path
)

:: ================
:: DOWNLOAD
:: ================
echo [+] Downloading NSSM...
powershell -NoLogo -NoProfile -Command ^
  "try { Invoke-WebRequest -Uri '%NSSM_URL%' -OutFile '%NSSM_ZIP%' -UseBasicParsing } catch { $host.SetShouldExit(1) }"
if errorlevel 1 (
  echo [!] Failed to download %NSSM_URL%
  exit /b 1
)

:: ================
:: EXTRACT nssm.exe
:: ================
echo [+] Extracting nssm.exe...
tar -xf "%NSSM_ZIP%" -C "%NSSM_DIR%" nssm-2.24\win64\nssm.exe >nul 2>&1
if errorlevel 1 (
  echo [i] tar not available; trying PowerShell Expand-Archive...
  powershell -NoLogo -NoProfile -Command ^
    "Expand-Archive -Path '%NSSM_ZIP%' -DestinationPath '%NSSM_DIR%' -Force"
  if errorlevel 1 (
    echo [!] Failed to extract NSSM zip.
    exit /b 1
  )
  if not exist "%NSSM_DIR%\nssm-2.24\win64\nssm.exe" (
    echo [!] nssm.exe not found in archive.
    exit /b 1
  )
  copy /Y "%NSSM_DIR%\nssm-2.24\win64\nssm.exe" "%NSSM_EXE%" >nul
) else (
  if exist "%NSSM_DIR%\nssm-2.24\win64\nssm.exe" (
    copy /Y "%NSSM_DIR%\nssm-2.24\win64\nssm.exe" "%NSSM_EXE%" >nul
  )
)

if not exist "%NSSM_EXE%" (
  echo [!] Could not place nssm.exe at "%NSSM_EXE%".
  exit /b 1
)

:: ================
:: ADD TO PATH (for future sessions)
:: ================
:add_to_path
echo [+] Adding "%NSSM_DIR%" to the user PATH (future terminals)...
for /f "tokens=2* delims= " %%A in ('reg query HKCU\Environment /v Path 2^>nul ^| find /I "Path"') do set "USERPATH=%%B"
echo %USERPATH% | find /I "%NSSM_DIR%" >nul
if errorlevel 1 (
  if defined USERPATH (
    set "NEWPATH=%USERPATH%;%NSSM_DIR%"
  ) else (
    set "NEWPATH=%NSSM_DIR%"
  )
  setx Path "%NEWPATH%" >nul
) else (
  echo [i] PATH already contains "%NSSM_DIR%".
)

:: ================
:: DONE
:: ================
"%NSSM_EXE%" -? >nul 2>&1
if errorlevel 1 (
  echo [i] NSSM installed at "%NSSM_EXE%". Open a NEW terminal to use it or call it by full path.
) else (
  echo ✅ NSSM installed: "%NSSM_EXE%"
  echo    Try: nssm --version   (in a NEW terminal)
)

endlocal
exit /b 0