param(
  [Parameter(Mandatory)] [string] $ServiceName,
  [Parameter(Mandatory)] [string] $ExePath,
  [string[]] $Arguments = @(),
  [string] $JsonArguments,                         # <--- NEW (preferred)
  [string] $WorkingDir,
  [string] $DisplayName,
  [string] $Description = "Managed by NSSM",
  [string] $LogDir = "C:\nssm\logs",
  [switch] $AutoStart,
  [switch] $StartNow,
  [int] $RestartDelayMs = 5000,
  [string] $ObjectName = "LocalSystem",
  [string] $ObjectPassword = ""
)

# --------- DEBUG / SAFETY GLUE (keeps window open) ----------
$ErrorActionPreference = 'Stop'
$VerbosePreference = 'Continue'
$log = Join-Path ([IO.Path]::GetTempPath()) ("nssm_create_" + ($ServiceName -replace '[^A-Za-z0-9_-]','_') + ".log")
try { Stop-Transcript | Out-Null } catch {}
Start-Transcript -Path $log -Append -Force | Out-Null

trap {
  Write-Host "`n[ERROR]" -ForegroundColor Red
  Write-Host ($_.Exception.Message)
  if ($_.InvocationInfo) { Write-Host ($_.InvocationInfo.PositionMessage) }
  if ($_.ScriptStackTrace) { Write-Host ($_.ScriptStackTrace) }
  Write-Host "`nLog file: $log"
  Read-Host "`nPress ENTER to close"
  Stop-Transcript | Out-Null
  exit 1
}
# ------------------------------------------------------------

Write-Host "[+] Create/Update NSSM service '$ServiceName'"

# Admin?
$IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $IsAdmin) { throw "Run this script as Administrator." }

# Prefer JSON for args (robust)
if ($JsonArguments) {
  try {
    $Arguments = @((ConvertFrom-Json -InputObject $JsonArguments))
  } catch {
    throw "JsonArguments is not valid JSON array. Example: ['C:\\apps\\myapp\\main.py','--port','8080']"
  }
}

# find nssm.exe
$nssm = "C:\nssm\nssm.exe"
if (-not (Test-Path $nssm)) {
  $cmd = Get-Command nssm.exe -ErrorAction SilentlyContinue
  if ($cmd) { $nssm = $cmd.Source } else { throw "nssm.exe not found (install to C:\nssm or add to PATH)" }
}
Write-Host "[DEBUG] NSSM   = $nssm"

# resolve paths
if (-not (Test-Path $ExePath)) { throw "ExePath not found: $ExePath" }
$ExePath = (Resolve-Path $ExePath).Path
if (-not $WorkingDir) { $WorkingDir = Split-Path $ExePath -Parent }
if (-not (Test-Path $WorkingDir)) { New-Item -ItemType Directory -Force -Path $WorkingDir | Out-Null }
$WorkingDir = (Resolve-Path $WorkingDir).Path
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }

Write-Host "[DEBUG] EXE    = $ExePath"
Write-Host "[DEBUG] CWD    = $WorkingDir"
Write-Host "[DEBUG] LOGDIR = $LogDir"
if ($Arguments.Count) { Write-Host "[DEBUG] ARGS   = $($Arguments -join ' ')" }

function Invoke-Nssm { param([string[]]$A)
  & $nssm @A
  if ($LASTEXITCODE -ne 0) { throw "nssm failed ($LASTEXITCODE): $($A -join ' ')" }
}

function Quote-Arg([string]$s){
  if ($s -match '[\s"]') { '"' + ($s -replace '"','\"') + '"' } else { $s }
}
$argsString = if ($Arguments.Count) { ($Arguments | ForEach-Object { Quote-Arg $_ }) -join ' ' } else { "" }

# create or update
$svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if (-not $svc) {
  Write-Host "[+] Installing service…"
  Invoke-Nssm (@('install', $ServiceName, $ExePath) + $Arguments)   # <-- each arg as its own element
} else {
  Write-Host "[i] Service exists; updating settings…"
  try { Invoke-Nssm @('stop', $ServiceName) } catch {}
}

# settings
Invoke-Nssm @('set', $ServiceName, 'AppDirectory', $WorkingDir)
if ($argsString) { Invoke-Nssm @('set', $ServiceName, 'AppParameters', $argsString) }
Invoke-Nssm @('set', $ServiceName, 'AppStdout', (Join-Path $LogDir "$ServiceName-stdout.log"))
Invoke-Nssm @('set', $ServiceName, 'AppStderr', (Join-Path $LogDir "$ServiceName-stderr.log"))
Invoke-Nssm @('set', $ServiceName, 'AppRotate', '1')
Invoke-Nssm @('set', $ServiceName, 'AppRotateBytes', '10485760')
Invoke-Nssm @('set', $ServiceName, 'AppRotateDelay', '10')
Invoke-Nssm @('set', $ServiceName, 'AppExit', 'Default', 'Restart')
Invoke-Nssm @('set', $ServiceName, 'AppRestartDelay', "$RestartDelayMs")

Invoke-Nssm @('set', $ServiceName, 'Start', ($AutoStart ? 'SERVICE_AUTO_START' : 'SERVICE_DEMAND_START'))

if ($DisplayName) { Invoke-Nssm @('set', $ServiceName, 'DisplayName', $DisplayName) }
if ($Description) { Invoke-Nssm @('set', $ServiceName, 'Description', $Description) }

if ($ObjectName -and $ObjectName -ne 'LocalSystem') {
  if (-not $ObjectPassword) { throw "ObjectPassword is required when ObjectName is not LocalSystem." }
  Invoke-Nssm @('set', $ServiceName, 'ObjectName', $ObjectName)
  Invoke-Nssm @('set', $ServiceName, 'Password',   $ObjectPassword)
} else {
  Invoke-Nssm @('set', $ServiceName, 'ObjectName', 'LocalSystem')
}

if ($StartNow) {
  Write-Host "[+] Starting service…"
  Invoke-Nssm @('start', $ServiceName)
  Start-Sleep -Seconds 1
  Get-Service -Name $ServiceName | Format-Table -Auto Name,Status,StartType
} else {
  Write-Host "[i] Not starting now (use -StartNow)."
}

Write-Host "`n✅ Done. Log: $log"
Read-Host "Press ENTER to close"
Stop-Transcript | Out-Null
