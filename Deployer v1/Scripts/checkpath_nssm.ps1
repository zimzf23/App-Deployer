# ======================
# uninstall_nssm.ps1
# ======================

$VerbosePreference = "Continue"
Write-Host "[+] NSSM Uninstaller starting..." -ForegroundColor Cyan

$dirsToCheck = @("C:\nssm", "$env:LOCALAPPDATA\nssm")

# --- Find existing nssm.exe ---
$found = @()
foreach ($d in $dirsToCheck) {
    $exe = Join-Path $d "nssm.exe"
    if (Test-Path $exe) { $found += $exe }
}

if (-not $found) {
    Write-Host "[i] NSSM not found in standard locations."
} else {
    Write-Host "[+] Found NSSM at:" -ForegroundColor Green
    $found | ForEach-Object { Write-Host "   $_" }

    foreach ($exe in $found) {
        $dir = Split-Path $exe -Parent
        try {
            Remove-Item -Path $dir -Recurse -Force -ErrorAction Stop
            Write-Host "  -> Removed $dir"
        } catch {
            Write-Warning "  !! Failed to remove $dir : $_"
        }
    }
}

# --- Clean PATH (User + Machine) ---
function Remove-FromPath($scope) {
    $p = [Environment]::GetEnvironmentVariable("Path",$scope)
    if (-not $p) { return }
    $parts = $p -split ";" | Where-Object { $_ -and ($_ -notmatch "^\s*$") }
    $new = $parts | Where-Object { $_ -notmatch "\\nssm$" }
    if ($new.Count -ne $parts.Count) {
        [Environment]::SetEnvironmentVariable("Path", ($new -join ";"), $scope)
        Write-Host "  -> Removed NSSM from $scope PATH"
    } else {
        Write-Host "  -> $scope PATH had no NSSM entry"
    }
}

Write-Host "[+] Cleaning PATH entries..."
Remove-FromPath "User"
Remove-FromPath "Machine"

# --- Refresh current session PATH ---
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ';' +
            [Environment]::GetEnvironmentVariable("Path","User")

Write-Host "`n✅ NSSM uninstalled."
Write-Host "   Run 'where.exe nssm' in a NEW terminal to confirm it is gone."

# === Pause at the end ===
Read-Host "`nPress ENTER to close"
