param(
  [Parameter(Mandatory)] [string] $ServiceName,
  [Parameter(Mandatory)] [string] $ExePath,
  [string[]] $Arguments = @(),
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

$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"
Write-Host "[+] Create/Update NSSM service '$ServiceName'"

# find nssm.exe
$nssm = "C:\nssm\nssm.exe"
if (-not (Test-Path $nssm)) {
  $cmd = Get-Command nssm.exe -ErrorAction SilentlyContinue
  if ($cmd) { $nssm = $cmd.Source } else { throw "nssm.exe not found (install to C:\nssm or add to PATH)" }
}
Write-Host "[DEBUG] NSSM = $nssm"

$ExePath = (Resolve-Path $ExePath).Path
if (-not $WorkingDir) { $WorkingDir = Split-Path $ExePath -Parent }
$WorkingDir = (Resolve-Path $WorkingDir).Path
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }

function Quote-Arg([string]$s){ if ($s -match '[\s"]') { '"' + ($s -replace '"','\"') + '"' } else { $s } }
$argsString = ($Arguments | ForEach-Object { Quote-Arg $_ }) -join ' '

$svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if (-not $svc) {
  Write-Host "[+] Installing service..."
  if ($argsString) { & $nssm install $ServiceName $ExePath $argsString | Out-Null }
  else             { & $nssm install $ServiceName $ExePath            | Out-Null }
} else {
  Write-Host "[i] Service exists; updating settings..."
  try { & $nssm stop $ServiceName | Out-Null } catch {}
}

& $nssm set $ServiceName AppDirectory $WorkingDir          | Out-Null
if ($argsString) { & $nssm set $ServiceName AppParameters $argsString | Out-Null }
& $nssm set $ServiceName AppStdout   (Join-Path $LogDir "$ServiceName-stdout.log") | Out-Null
& $nssm set $ServiceName AppStderr   (Join-Path $LogDir "$ServiceName-stderr.log") | Out-Null
& $nssm set $ServiceName AppRotate   1                 | Out-Null
& $nssm set $ServiceName AppRotateBytes 10485760       | Out-Null
& $nssm set $ServiceName AppRotateDelay 10             | Out-Null
& $nssm set $ServiceName AppExit Default Restart       | Out-Null
& $nssm set $ServiceName AppRestartDelay $RestartDelayMs | Out-Null

if ($AutoStart) { & $nssm set $ServiceName Start SERVICE_AUTO_START | Out-Null }
else            { & $nssm set $ServiceName Start SERVICE_DEMAND_START | Out-Null }

if ($DisplayName) { & $nssm set $ServiceName DisplayName $DisplayName | Out-Null }
if ($Description){ & $nssm set $ServiceName Description $Description  | Out-Null }

if ($ObjectName -and $ObjectName -ne "LocalSystem") {
  if (-not $ObjectPassword) { throw "ObjectPassword is required when ObjectName is not LocalSystem." }
  & $nssm set $ServiceName ObjectName $ObjectName     | Out-Null
  & $nssm set $ServiceName Password   $ObjectPassword | Out-Null
} else {
  & $nssm set $ServiceName ObjectName LocalSystem     | Out-Null
}

if ($StartNow) {
  Write-Host "[+] Starting service..."
  & $nssm start $ServiceName | Out-Null
  Start-Sleep -Seconds 1
  Get-Service -Name $ServiceName | Format-Table -AutoSize Name,Status,StartType
} else {
  Write-Host "[i] Not starting now (use -StartNow to start)."
}

Write-Host "`n✅ Done."
Read-Host "Press ENTER to close"
