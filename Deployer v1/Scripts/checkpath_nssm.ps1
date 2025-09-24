<#  fix-nssm-path.ps1
    Checks and fixes PATH for NSSM, refreshes current session, and broadcasts env change.
    Usage:
      # just fix user PATH + current session
      .\fix-nssm-path.ps1

      # also ensure Machine (system) PATH (run as Admin)
      .\fix-nssm-path.ps1 -Machine

      # or specify a custom install dir explicitly
      .\fix-nssm-path.ps1 -Dir "C:\nssm" -Machine
#>

param(
  [string]$Dir,
  [switch]$Machine
)

$VerbosePreference = "Continue"
Write-Host "[+] NSSM PATH fixer starting..." -ForegroundColor Cyan

function Get-NssmDir {
  param([string]$Preferred)
  if ($Preferred) {
    if (Test-Path (Join-Path $Preferred 'nssm.exe')) { return ($Preferred.TrimEnd('\')) }
    Write-Warning "Preferred dir '$Preferred' does not contain nssm.exe"
  }
  $candidates = @(
    'C:\nssm',
    "$env:LOCALAPPDATA\nssm"
  )
  foreach ($d in $candidates) {
    if (Test-Path (Join-Path $d 'nssm.exe')) { return ($d.TrimEnd('\')) }
  }
  $cmd = Get-Command nssm.exe -ErrorAction SilentlyContinue
  if ($cmd) { return ((Split-Path $cmd.Source -Parent).TrimEnd('\')) }
  return $null
}

function Add-ToPath {
  param(
    [Parameter(Mandatory)] [string]$PathDir,
    [Parameter(Mandatory)] [ValidateSet('User','Machine')] [string]$Scope
  )
  $PathDir = $PathDir.TrimEnd('\')
  $cur = [Environment]::GetEnvironmentVariable('Path', $Scope)
  if (-not $cur) { $cur = '' }
  $parts = $cur -split ';' | Where-Object { $_ } | ForEach-Object { $_.Trim() }
  $norm  = $parts | ForEach-Object { $_.TrimEnd('\') }

  if ($norm -contains $PathDir) {
    Write-Host "  -> $Scope PATH already contains $PathDir"
    return $false
  }

  $new = ($cur.TrimEnd(';') + ';' + $PathDir).Trim(';')
  [Environment]::SetEnvironmentVariable('Path', $new, $Scope)
  Write-Host "  -> $Scope PATH updated (added $PathDir)"
  return $true
}

function Broadcast-Env {
  $sig = @"
using System;
using System.Runtime.InteropServices;
public static class EnvBroadcast {
  [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
  public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, IntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out IntPtr lpdwResult);
}
"@
  Add-Type $sig -ErrorAction SilentlyContinue | Out-Null
  [IntPtr]$r = [IntPtr]::Zero
  [void][EnvBroadcast]::SendMessageTimeout([IntPtr]0xffff, 0x1A, [IntPtr]0, 'Environment', 2, 5000, [ref]$r)
  Write-Host "  -> Broadcasted ENV change to system"
}

# --- Detect dir ---
$NssmDir = Get-NssmDir -Preferred $Dir
if (-not $NssmDir) {
  Write-Host "[!] Could not find nssm.exe automatically." -ForegroundColor Yellow
  Write-Host "    If you know the folder, run: .\fix-nssm-path.ps1 -Dir 'C:\path\to\nssm'"
  Read-Host "`nPress ENTER to close"
  exit 1
}

$exe = Join-Path $NssmDir 'nssm.exe'
Write-Host "[DEBUG] NSSM_DIR = $NssmDir"
Write-Host "[DEBUG] NSSM_EXE = $exe"
if (-not (Test-Path $exe)) {
  Write-Host "[!] $exe not found. Nothing to do." -ForegroundColor Yellow
  Read-Host "`nPress ENTER to close"
  exit 1
}

# --- Ensure PATH (User) ---
$changed = $false
$changed = (Add-ToPath -PathDir $NssmDir -Scope 'User') -or $changed

# --- Ensure PATH (Machine) if requested/possible ---
$elevated = $false
try { $elevated = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) } catch {}
if ($Machine) {
  if ($elevated) {
    $changed = (Add-ToPath -PathDir $NssmDir -Scope 'Machine') -or $changed
  } else {
    Write-Host "  -> Not elevated: skipping Machine PATH (run PowerShell as Administrator or omit -Machine)" -ForegroundColor Yellow
  }
}

# --- Refresh THIS session PATH so nssm works immediately ---
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
            [Environment]::GetEnvironmentVariable('Path','User')
Write-Host "  -> Current session PATH refreshed"

# --- Broadcast env change for future apps/terminals ---
if ($changed) { Broadcast-Env } else { Write-Host "  -> No PATH registry changes made" }

# --- Verify ---
Write-Host "`n[VERIFY]"
try {
  where.exe nssm | ForEach-Object { Write-Host "where.exe: $_" }
} catch { Write-Host "where.exe couldn't find nssm" -ForegroundColor Yellow }
$cmds = Get-Command nssm -ErrorAction SilentlyContinue
if ($cmds) { $cmds | Format-Table -AutoSize Source,CommandType } else { Write-Host "Get-Command: not found" -ForegroundColor Yellow }

Write-Host "`n[RUN]"
try {
  nssm --version
} catch {
  Write-Host "Failed to run 'nssm --version' in this session." -ForegroundColor Yellow
  Write-Host "You can still run with full path: `"$exe --version`""
}

Write-Host "`n✅ Done. If an embedded terminal still fails, restart its host app (VS Code, PyCharm, Windows Terminal)."
Read-Host "`nPress ENTER to close"
